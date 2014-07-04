from celery import Celery

__author__ = 'nebras'

from django.conf import settings
from WebDev.models import  Pipeline, Results , RunningProcess
from django.core.files import File

import csv
import multiprocessing
import numpy
import optparse
import os
import re
import subprocess
import sys
import tempfile
import time
import uuid

app = Celery('tasks', broker='amqp://localhost//')

@app.task
def prepro(self, uniqueJobID, listofSFFfiles, listOfMappingFiles):
    '''
    :param UniqueJobID: Stuff that Hiromu Needs for his script.
    :param ListofSFFfiles:
    :param ListOfMappingFiles:
    :return:
    '''

    tmpdir = str(Pipeline.pip_id)
    result_path = os.path.join(settings.MEDIA_ROOT, settings.RESULT_PATH)
    result_path_full = os.path.join(result_path, tmpdir)
    media_path = os.path.join(settings.RESULT_PATH, tmpdir)
        if not os.path.exists(result_path_full):
        os.makedirs(result_path_full)

    print "Running"
    self.update_state(state='RUNNING', meta='Preprocessing...')
    t = preprocess(uniqueJobID, listofSFFfiles , listOfMappingFiles)

    try:
         resdb = Results(
                        process_name=pname,
                        filepath=result_path_full,
                        filetype=tp,
                        filename=myn,
                        task_id = RunningProcess.objects.get(task_id=self.request.id)
                    )

        resdb.filepath= t
        resdb.process_name= preprocessing
        resdb.filetype= 'txt'

        except Exception, error:
                    print error

    try:
                        resdb.save()
                    except Exception, e:
                        print e

    return True

def preprocess(job_id, sff, mapping):
    '''
    :param job_id: unique job id (used for result filename)
    :param sff: list of input sff files
    :param mapping: list of input mapping files
    :return: file name of otu table
    '''
    core = multiprocessing.cpu_count() - 1

    pipeline = SFF2OTU(job_id, sff, mapping)
    return os.path.abspath(pipeline.run(processors = core))

class SFF2OTU:
    def __init__(self, job_id, sff, mapping):
        if isinstance(sff, str):
            sff = [sff]
        if isinstance(mapping, str):
            mapping = [mapping]

        if len(sff) != len(mapping):
            raise ValueError, 'the number of sff files and oligo files must be same'

        self.job_id = job_id
        self.sff = sff
        self.mapping = mapping

        self.dir = tempfile.mkdtemp()
        self.fasta_dir = tempfile.mkdtemp()

        self.fasta = []
        self.qual = []
        self.oligo = []

        self.trim_fasta = []
        self.group = []

    def __del__(self):
        import shutil
        shutil.rmtree(self.dir)
        shutil.rmtree(self.fasta_dir)

    def run(self, processors = 1, *args, **kwargs):
        kwargs['processors'] = processors

        self.sffinfo()
        self.map2oligo()
        self.trim(kwargs)
        self.split()

        mapfile = self.merge_map()
        self.merge_fasta(mapfile)
        self.pick_otus(processors)
        taxa_otu = self.summarize_taxa()
        return self.merge_otu(taxa_otu)

    def command(self, args):
        process = subprocess.Popen(args, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        retcode = process.wait()
        if retcode != 0:
            sys.stderr.write(process.stderr.read())
            raise IOError, '%s raises error: %d' % (args[0], retcode)
        return process.stdout.readlines()

    def mothur(self, outdir, command):
        command = '#set.dir(output=%s); set.logfile(name=%s); %s' % (outdir, os.devnull, command)
        output = self.command(['mothur', command])
        if 'Output File Names: \n' not in output:
            raise IOError, 'mothur didn\'t output anything'
        return output

    def sffinfo(self):
        for sff in self.sff:
            command = 'sffinfo(sff=%s,fasta=T,qfile=T,sfftxt=F,flow=F)' % sff
            output = self.mothur(self.dir, command)

            for line in output[output.index('Output File Names: \n') + 1:]:
                if not line:
                    break
                if line.strip().endswith('fasta'):
                    self.fasta.append(line.strip())
                elif line.strip().endswith('qual'):
                    self.qual.append(line.strip())

    def map2oligo(self):
        for mapping in self.mapping:
            data = numpy.loadtxt(mapping, dtype = 'string')
            output = os.path.join(self.dir, os.path.splitext(os.path.basename(mapping))[0] + '.oligo')

            with open(output, 'w') as oligo:
                writer = csv.writer(oligo, delimiter = '\t', lineterminator = '\n')
                writer.writerow(['forward', data[0, 2]])

                for i in xrange(data.shape[0]):
                    writer.writerow(['barcode', data[i, 1], data[i, 0]])
            
            self.oligo.append(output)

    def trim(self, kwargs):
        if not len(self.fasta) == len(self.qual) == len(self.oligo):
            raise ValueError, 'sffinfo and map2oligo must be executed before trim'
        
        for fasta, qual, oligo in zip(self.fasta, self.qual, self.oligo):
            kwargs['fasta'] = fasta
            kwargs['oligos'] = oligo
            kwargs['qfile'] = qual
            options = ','.join([str(i[0]) + '=' + str(i[1]) for i in kwargs.items()])

            command = 'trim.seqs(%s)' % options
            output = self.mothur(self.dir, command)

            for line in output[output.index('Output File Names: \n') + 1:]:
                if not line:
                    break
                if line.strip().endswith('trim.fasta'):
                    self.trim_fasta.append(line.strip())
                elif line.strip().endswith('groups'):
                    self.group.append(line.strip())

    def split(self):
        if len(self.trim_fasta) != len(self.group):
            raise ValueError, 'trim must be executed before split'

        for trim, group in zip(self.trim_fasta, self.group):
            command = 'split.groups(fasta=%s,group=%s)' % (trim, group)
            output = self.mothur(self.fasta_dir, command)

    def merge_map(self):
        if len(self.trim_fasta) != len(self.mapping):
            raise ValueError, 'trim must be executed before split'

        mapfile = os.path.join(self.dir, 'merged.map')
        with open(mapfile, 'w') as output:
            writer = csv.writer(output, delimiter = '\t', lineterminator = '\n')
            writer.writerow(["#SampleID", "BarcodeSequence", "LinkerPrimerSequence", "Path", "Class", "Description"])

            for mapping, trim in zip(self.mapping, self.trim_fasta):
                data = numpy.loadtxt(mapping, dtype = 'string')
                for i in xrange(data.shape[0]):
                    filename = os.path.splitext(os.path.basename(trim))[0] + '.' + data[i, 0] + '.fasta'
                    writer.writerow(data[i, 0: 3].tolist() + [filename] + data[i, 3:].tolist())

        return mapfile

    def merge_fasta(self, mapfile):
        self.command(['add_qiime_labels.py', '-m', mapfile, '-i', self.fasta_dir, '-c', 'Path', '-o', self.dir])

    def pick_otus(self, parallel):
        combined = os.path.join(self.dir, 'combined_seqs.fna')
        self.command(['pick_de_novo_otus.py', '-i', combined, '-o', self.dir, '-f', '-a', '-O', str(parallel)])

    def summarize_taxa(self):
        biom = os.path.join(self.dir, 'otu_table.biom')
        taxa_out = os.path.join(self.dir, 'taxa_out')
        self.command(['summarize_taxa.py', '-i', biom, '-o', taxa_out])
        return taxa_out

    def merge_otu(self, taxa_out):
        line = None
        data = None

        for otu in os.listdir(taxa_out):
            if not re.search('L[0-9]*.txt$', otu):
                continue

            matrix = numpy.loadtxt(os.path.join(taxa_out, otu), dtype = str, delimiter = '\t')
            if line == None:
                line = matrix[0]

            if data == None:
                data = matrix[1:]
            else:
                data = numpy.concatenate((data, matrix[1:]))

        line[0] = '#OTU ID'
        data = numpy.append(data, data[:, 0].reshape(len(data), 1),axis = 1)
        for i in xrange(len(data)):
            data[i, 0] = 'merged' + str(i)

        otu_table = os.path.join(os.path.dirname(self.sff[0]), self.job_id + '.otu_table.txt')
        with open(otu_table, 'w') as output:
            writer = csv.writer(output, delimiter = '\t', lineterminator = '\n')
            writer.writerow(line)
            for line in data:
                writer.writerow(line)

        return otu_table
