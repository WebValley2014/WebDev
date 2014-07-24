#!/usr/bin/env python

import csv
import os
import numpy
import shutil
import subprocess
import sys
import tempfile
import uuid

import plot_metrics

class ML:
    def __init__(self, job_id, otu_file, class_file):
        self.otu_file = otu_file
        if not os.path.exists(self.otu_file):
            raise IOError, 'file doesn\'t exists: %s' % self.otu_file

        self.class_file = class_file
        if not os.path.exists(self.class_file):
            raise IOError, 'file doesn\'t exists: %s' % self.class_file

        self.job_id = job_id
        self.dir = tempfile.mkdtemp()
        self.result = {}
        self.feat_str ='' #string with features from kwargs

    def __del__(self):
        import shutil
        shutil.rmtree(self.dir)

    def run(self, percentage = 10, n_groups = 10, scaling = 'std', solver = 'l2r_l2loss_svc', ranking = 'SVM', *args, **kwargs):
        #print percentage
        #print n_groups
        #print scaling
        #print solver
        #print ranking
        #print args
        #print kwargs
        
        self.differentiate_path(percentage, n_groups, scaling, solver, ranking, **kwargs)
        
        #print self.feat_str
        
        self.job_id+=self.feat_str
        
        #print self.job_id
        
        otu_table = self.filter_otu(percentage)
        matrix, classes = self.convert_input(otu_table)
        
        #print otu_table
        #print matrix
        #print classes
        
        #OTUS=numpy.loadtxt(matrix,delimiter='\t',dtype=str)
        #print OTUS
        
        #CLASSES=numpy.loadtxt(classes,delimiter='\t',dtype=str)
        #print CLASSES
        
        self.machine_learning(matrix, classes, scaling, solver, ranking, kwargs)
        
        #print self.result
        
        #print numpy.loadtxt(self.result['metrics'],delimiter='\t',dtype=str,skiprows=1)
        
        self.process_otu_table(n_groups, classes)
        self.phylo3d()

        self.result['img'] = os.path.join(os.path.dirname(self.otu_file), 'img')
        graph = plot_metrics.BacteriaGraph(self.result['metrics'])
        graph.printAllPlots(self.result['img'])

	      
        #print self.result
        
        #print numpy.loadtxt(self.result['metrics'],delimiter='\t',dtype=str,skiprows=1)
        

        return self.result, self.feat_str
        

    def command(self, args):
        #process = subprocess.Popen(args, stdout=sys.__stdout__, stderr=sys.__stderr__) #, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        process = subprocess.Popen(args, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        retcode = process.wait()
        if retcode != 0:
            sys.stderr.write(process.stderr.read())
            raise IOError, '%s raises error: %d' % (args[0], retcode)
        return process.stdout.readlines()   #

    def filter_otu(self, percentage):
        script = os.path.join(os.path.dirname(__file__), 'ml', 'feat_filter.py')
        out_file = os.path.join(self.dir, 'filtered_otu.txt')
        process = self.command(['python', script, '-i', self.otu_file, '-o', out_file, '-p', str(percentage)])

        self.result['filtered_otu'] = os.path.join(os.path.dirname(self.otu_file), self.job_id + '.otu_filtered.txt')
        shutil.copyfile(out_file, self.result['filtered_otu'])

        return out_file
        
    def NONOconvert_input(self, otu_file):
		
		otutable=numpy.loadtxt(otu_file, delimiter='\t',dtype=str,comments='^')
		table=otutable.transpose(1,0)
		table[0]=table[-1]
		table=table[:-1]
		table[0,0]='Sample ID'
		print table
		table_list=table.tolist()
		#sort table and then export
		#Ys
		
		return 0,0
		
		
#INDENTATION
		
		
		
    def convert_input(self, otu_file):
        features = []
        samples = None
        data = None

        with open(otu_file) as otu:
            reader = csv.reader(otu, delimiter = '\t')

            line = []
            while len(line) == 0 or line[0] != '#OTU ID':
                line = reader.next()
            samples = line[1: -1]

            for line in reader:
                features.append(line[-1])
                if data == None:
                    data = line[1: -1]
                else:
                    data = numpy.vstack((data, line[1: -1]))
        
            data = numpy.transpose(data, (1, 0))
            data = numpy.hstack((numpy.array(samples).reshape(len(samples), 1), data))

        classes = numpy.loadtxt(self.class_file, dtype = str)
        if len(classes[0]) > 1:
            #classes.sort(axis = 0)
            #data.sort(axis = 0)
            c_L=classes.tolist()
            d_L=data.tolist()
            c_L.sort()
            d_L.sort()
            classes=numpy.array(c_L)
            data=numpy.array(d_L)
            #classes=numpy.array(classes.tolist().sort())
            #data=numpy.array(data.tolist().sort())

        matrix_txt = os.path.join(self.dir, 'matrix.txt')
        classes_txt = os.path.join(self.dir, 'classes.txt')

        with open(matrix_txt, 'w') as output:
            writer = csv.writer(output, delimiter = '\t', lineterminator = '\n')
            writer.writerow(['Sample ID'] + features)
            for line in data:
                writer.writerow(line)

        with open(classes_txt, 'w') as output:
            writer = csv.writer(output, delimiter = '\t', lineterminator = '\n')
            for line in classes:
                writer.writerow(line[-1])

        return matrix_txt, classes_txt

    def machine_learning(self, matrix, classes, scaling, solver, ranking, kwargs):
        script = os.path.join(os.path.dirname(__file__), 'ml', 'svmlin_training.py')

        options = []
        for key, value in kwargs.items():
			if key=='random':
				if value==True:
					options.append('--' + key)
			else:					 
				options.append('--' + key)
			if not isinstance(value, bool):
				options.append(str(value))
        
        print "OPTIONS"
        print options
        
		
        outdir = os.path.join(self.dir, 'out')
        os.mkdir(outdir)
        
        #print ['python', script, matrix, classes, scaling, solver, ranking] + options + [outdir]
        
        process = self.command(['python', script, matrix, classes, scaling, solver, ranking] + options + [outdir])

        prefix = os.path.join(os.path.dirname(self.otu_file), self.job_id + '.')
        
        print prefix
       
        
        for filename in os.listdir(outdir):
            for suffix in ['featurelist', 'metrics', 'stability']:
                if filename.endswith(suffix + '.txt'):
                    output = prefix + suffix + '.txt'
                    shutil.copyfile(os.path.join(outdir, filename), output)
                    self.result[suffix] = output
                                        
        #print self.result
        
                    

    def process_otu_table(self, n_groups, classes):
        feature_names = numpy.loadtxt(self.result['featurelist'], dtype = str, skiprows = 1, usecols = (0, 1))
        ranked = feature_names[:, 1]

        whole_table = numpy.loadtxt(self.result['filtered_otu'], dtype = str, delimiter = '\t', comments = '^')
        name_column = whole_table[:, -1]

        processed_table = numpy.zeros((n_groups + 2, len(whole_table[1, :])), dtype = 'S512')
        processed_table[0,:] = whole_table[0,:]

        labels = numpy.loadtxt(classes, dtype = str, delimiter = '\n')
        processed_table[1, 0] = 'Label'
        processed_table[1, 1: -1] = labels

        current_row = 2
        for f in ranked[:n_groups]:
            for i in range(1, len(name_column)):
                if f in name_column[i] and current_row <= n_groups:
                    processed_table[current_row, :] = whole_table[i, :]
                    current_row += 1

        processed_table.transpose()

        self.result['otu'] = os.path.join(os.path.dirname(self.otu_file), self.job_id + '.otu_table.txt')
        numpy.savetxt(self.result['otu'], processed_table, delimiter = '\t', fmt = '%s')

    def phylo3d(self):
        script = os.path.join(os.path.dirname(__file__), 'phylo3D', 'import.py')
        xml = os.path.join(self.dir, 'dendro.xml')
        process = self.command(['python', script, self.result['featurelist'], xml])

        script = os.path.join(os.path.dirname(__file__), 'phylo3D', 'process.py')
        self.result['json'] = os.path.join(os.path.dirname(self.otu_file), self.job_id + '.json')
        process = self.command(['python', script, xml, self.result['featurelist'], self.result['json']])
    def differentiate_path(self,percentage, n_groups, scaling, solver, ranking, **kwargs):
		#feat_str='__'
		feat_str=''
		feat_str+=str(scaling)
		feat_str+='_'+str(solver)
		feat_str+='_'+str(ranking)
		feat_str+='_'+str(scaling)
		if 'cv_n' in kwargs:
			feat_str+='_cv_n_'+str(kwargs['cv_n'])
		if 'cv_k' in kwargs:
			feat_str+='_cv_k_'+str(kwargs['cv_k'])
		feat_str+='_'+str(percentage)+'_percent'
		if 'random' in kwargs:
			if kwargs['random']:
				feat_str+='_random'
		#feat_str+='_'
		feat_str=feat_str.replace('_','-')
		self.feat_str=feat_str
		return feat_str
		
		

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage: %s [DATA_FILE] [CLASS_FILE]' % sys.argv[0]
        sys.exit(-1)

    job_id = str(uuid.uuid4())
    ml = ML(job_id, sys.argv[1], sys.argv[2])
    print(ml.run())
