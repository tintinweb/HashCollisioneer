'''
Created on Apr 23, 2012

@author: tintinweb
'''
from collections import Counter

def crc16(buff, crc = 0, poly = 0xa001):
    l = len(buff)
    i = 0
    while i < l:
        ch = ord(buff[i])
        uc = 0
        while uc < 8:
            if (crc & 1) ^ (ch & 1):
                crc = (crc >> 1) ^ poly
            else:
                crc >>= 1
            ch >>= 1
            uc += 1
        i += 1
    return crc

def crc16str(s,poly=0x1021):
    crc = 0
    for index1 in range(len(s)):
        crc = crc ^ (ord(s[index1]) << 8)
        for index2 in range(1, 9):
            if crc & 0x8000 != 0:
                crc = ((crc << 1) ^ poly)
            else:
                crc = crc << 1
    return crc & 0xFFFF

def crc16netsnmp9rounds(s):
    crc=0
    i=0
    i2=0
    for i in range(len(s)):
        crc = crc ^ (ord(s[i])<<8)
        for i2 in range(9):
            if (crc & 0x8000)!=0:
                crc=(crc<<1)^0x1021
            else:
                crc = crc << 1
    return crc & 0xffff

def crc16netsnmp8rounds(s):
    crc=0
    i=0
    i2=0
    for i in range(len(s)):
        crc = crc ^ (ord(s[i])<<8)
        for i2 in range(8):
            if (crc & 0x8000)!=0:
                crc=(crc<<1)^0x1021
            else:
                crc = crc << 1
    return crc & 0xffff
    
def ELFHash0x10000(key):
    hash = 0
    x = 0
    for i in range(len(key)):
        hash = (hash << 4) + ord(key[i])
        x = hash & 0xF0000000
        if x != 0:
            hash ^= (x >>24)
        hash &= ~x
        
    return hash % 65536

def ELFHash0xffff(key):
    hash = 0
    x = 0
    for i in range(len(key)):
        hash = (hash << 4) + ord(key[i])
        x = hash & 0xF0000000
        if x != 0:
            hash ^= (x >>24)
        hash &= ~x
        
    return hash % 65535
#hash & 0x7FFFFFFF) %


def diff_list_cnt(a,numHits=2):
    result={}
    xx = Counter(a).most_common()
    
    for (k,v) in xx:
        if v>=numHits: result[k]=v
        
    return result

def iterHash(prefix,numHashes,hashfunc=ELFHash0x10000):
    hashes=[]
    #print "--creating hashlist: %s--"%prefix
    #hashes.append(tuple([ELFHash(prefix),prefix]))
    hashes.append(tuple([hashfunc(prefix),prefix]))
    for i in range(0,numHashes):
        elfhash=hashfunc("%s%d"%(prefix,i))
        hashes.append(tuple([elfhash,"%s%d"%(prefix,i)]))
        #if i % 50000 == 0: print i
    #print i
    return hashes

def getHashes_only(data):
    result = []
    for elem in data:
        hash,data=elem
        result.append(hash)
    return result

def find_hash(data,h):
    result = []
    for hash,name in data:
        if hash==h: result.append((hash,name))
    return result

if __name__=="__main__":
    performance=[]
    hashfuncs=[ELFHash0x10000,ELFHash0xffff,crc16str,crc16,crc16netsnmp9rounds,crc16netsnmp8rounds]
    num=128   
    
    for hf in hashfuncs:
        print "[*] collisiontest for %s"%hf.__name__
        hashes = iterHash("eth",num,hf)
        hashes += iterHash("port",num,hf)
        hashes += iterHash("p",num,hf)
        hashes += iterHash("lo",5,hf)
        hashes += iterHash("a",num,hf)
        hashes += iterHash("b",num,hf)
        hashes += iterHash("c",num,hf)
        hashes += iterHash("A",num,hf)
        hashes += iterHash("B",num,hf)
        hashes += iterHash("C",num,hf)
        hashes += iterHash("portA",num,hf)
        hashes += iterHash("portB",num,hf)
        hashes += iterHash("portC",num,hf)
        
        
        hh=getHashes_only(hashes)
        print "--coarse dupecheck--"
        print len(hh)
        print len(set(hh))
        print "--finegrained dupecheck / diff--"
        #print diff_list_self(hashes)
        diffs= diff_list_cnt(hh)
        for k,v in diffs.iteritems():
            print find_hash(hashes,k)
            pass
        print "--------------------------------------\n\n"
        
        performance.append((hf.__name__,len(hh),len(set(hh))))
    print "--done--"
    print "\n"
    print "Hashfunc\t|\tPerformance\t(100%=best, no collisions in testset)"
    for h,pmax,pmin in performance: print "%s\t|\t%f%% (%d/%d)"%(h,float(pmin*100)/float(pmax),pmin,pmax)
    
    
    print "----"
