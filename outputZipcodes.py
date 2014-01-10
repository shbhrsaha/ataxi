'''
Created on Oct 8, 2013
COS 455, HW 1, Problem 5.1 "Fetching Sequences with BioPython"

@author: John
'''
import os, re, sys, csv, numpy, scipy.spatial

''' for each line in input file, create output file using first entry,
then query entrez on each subsequent entry and save results '''
def genZipcodeDict(zipcodeCSV):
    #read input into list
    latLongToZip = {}
    with open(zipcodeCSV, 'rb') as csvfile:
        zipreader = csv.DictReader(csvfile)
        for zipMetadata in zipreader:
            #print (float(zipMetadata['latitude']),float(zipMetadata['longitude']))
            #print zipMetadata
            latLongToZip[(float(zipMetadata['latitude']),float(zipMetadata['longitude']))] = int(zipMetadata['zip'])

    csvfile.close()
    return latLongToZip

if __name__ == '__main__':
    # check for legal number of args
    if len(sys.argv) != 3:
        sys.exit("expect cmd args: python %s <zipcode.csv> <NORModule7NN.csv> " % sys.argv[0])
    # read command args
    zipcodeCSV = sys.argv[1];
    NN_CSV = sys.argv[2];
    
    # takes tuple (centroid-lat, centroid-long), returns zipcode
    latLongToZip = genZipcodeDict(zipcodeCSV)
    # can be queried for nearest centroid to a point
    centroidTree=scipy.spatial.cKDTree(numpy.asarray(list(latLongToZip.keys())),leafsize=30)
    
    LAT_IDX = 3; LONG_IDX = 4;
    with open(NN_CSV, 'rb') as csvfile:
        NN_reader = csv.reader(csvfile)
        for NN_metadata in NN_reader:
            (dist, centroid_IDX) = centroidTree.query([float(NN_metadata[LAT_IDX]), float(NN_metadata[LONG_IDX])], k=1, distance_upper_bound = 10);
            zip = latLongToZip[(centroidTree.data[centroid_IDX,0], centroidTree.data[centroid_IDX,1])]
            print('(lat, long) is (%f, %f)\n\t closest centroid is %s, has zipcode %d, and is %f away \n' % (float(NN_metadata[LAT_IDX]), float(NN_metadata[LONG_IDX]), centroidTree.data[centroid_IDX,:], zip, dist))
    #Play with the leafsize to get the fastest result for your dataset
