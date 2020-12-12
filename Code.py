# CD Python Project Code 2020
# Made by Tanmay Gupta (2018UCP1349) and Akash Sharma (2018UCP1154)
# Submitted to Dinesh Goplani Sir


def non(k):
    if k=="^":
        return ""
    return k    

def check(k):
    if ord(k)<=ord("Z") and ord(k)>=ord("A"):
        return True
    return False    

# Variable Initialization 
d={}
symbol=set()
prod={}
prod1={}

print("Enter the size of the productions : ")
n=int(input())

print("Enter productions : ")
for i in range(n):
    x,y=map(str,input().split())
    
    symbol=symbol.union(set(list(x)))
    symbol=symbol.union(set(list(y)))
    #checking validity of grammar
    if not  (ord(x)<=ord("Z") and ord(x)>=ord("A")):
        print("Invalid Grammar")
        exit()
    d[x]=d.get(x,[]) + [y]
    prod[str(x)+str(y)]=i
    prod1[i]=str(x)+str(y)
if "^" in symbol:
    symbol.remove("^")
    

first={}
vis={}

for i in d:
    first[i]=set()
    for j in d[i]:
        # print(j)
        if not check(j[0]):
            first[i].add(j[0])          

#find first
def find_first(k):
    
    # print(k,first)
    vis[k]=1    
    for i in d[k]:
        for j in range(len(i)):
            if check(i[0]):
                b={}
                if not check(i[j]):
                    first[k].add(i[j])
                    break
                elif i[j] not in vis:
                    vis[i[j]]=1
                    
                    find_first(i[j])
                    b=first[i[j]].copy()
                elif i[j] in vis:
                    b=first[k].copy()
                if "^" not in b:
                    first[k]=first[k].union(first[i[j]])
                    # first[k]=first[k].union(b)
                    break
                elif j!=len(i)-1:
                    b.remove("^")
                    first[k]=first[k].union(b)
                    
                else:
                    first[k]=first[k].union(first[i[j]])                
            
    vis[k]=-1                

for j in d:
    find_first(j)
    
print("\t FIRSTS \n")
for i in first:
    print(i,"\t",first[i])
    
print()

follow={}
for i in d:
    follow[i]=set()

# follow of start symbol is $
follow["S"]={"$"}
vis1={}

# find follow
def find_follow(k):
    vis[k]=1
    for i in d:
        for j in d[i]:
            for ind in range(len(j)):
                if j[ind]==k:
                    for ind1 in range(ind+1,len(j)):
                        if not check(j[ind1]):
                            follow[k].add(j[ind1])
                            break
                        elif  "^" not in  first[j[ind1]]:
                            follow[k]=follow[k].union(first[j[ind1]])
                            break
                        elif "^" in  first[j[ind1]]:
                            b=first[j[ind1]].copy()
                            # print(b,first[j[ind1]])
                            b.remove("^")
                            follow[k]=follow[k].union(b)
                    else:
                        if i not in vis:
                            find_follow(i)
                        
                        b=follow[i]
                        follow[k]=follow[k].union(b)
    
    vis[k]=-1
    
for i in d:
    find_follow(i)
    
print("\t FOllow \n")
for i in follow:
    print(i,"\t",follow[i])
    
print()
d["S'"]=["S"]
# finding closure
def closure(s):
    vis={}
    a=[]
    b=[]
    for i in s:
        a.append(i)
        vis[(i[0]) + (i[1])]=1
    while a:
        # print(a)
        j=a.pop(0)
        i=j[1]
        b.append(j)
        # print(i)
        if i.index(".") + 1<len(i) and i[i.index(".") + 1] in d:
            for k in d[i[i.index(".") + 1]]:
                if i[i.index(".") + 1] + k not in vis:
                    vis[i[i.index(".") + 1] + k]=1
                    a.append([i[i.index(".") + 1],"."+ non(k) ])
                    
    return b

def goto(a,x):
    b=[]
    for j in a:
        i=j[1]
        ind=i.index(".")
        if i.index(".") + 1<len(i) and i[i.index(".") + 1] == x:
            k=[j[0],i[:ind] + i[ind+1] + "." + i[ind+2:]]
            if k not in b:
                b.append(k)
            
    return closure(b)

state=[[-1] for i in range(50)]

state[0]=closure([["S'",".S"]])
i=0
ind=1
vis={}
arr={}
vis[ind]=sorted(state[0])
sp=0
# finding total no of sstates
while state[i]!=[-1]:
    for k in symbol:
        b=[]
        for j in state[i]:
            c=goto([j],k)
            if j[0]=="S'":
                sp=i
            if len(c)!=0:
                b+=c[:]
                
        if b !=[]:        
            for kk in vis:
                if sorted(b)==vis[kk]:
                    arr[(i,k)]=kk
                    break
            else:
                state[ind]=b[:]
                arr[(i,k)]=ind
                vis[ind]=sorted(b[:])
                ind+=1
    i += 1
total_st=i

# print total states
print("\nTotal States = ",total_st)

table={}
inf=10**12
for i in symbol:
    table[i]=["_" for j in range(total_st)]
table["$"]=["_" for j in range(total_st)]

# checking Grammar is Ambiguous or not
for i in arr:
    if table[i[1]][i[0]]!="_":
        print("Ambiguous Grammar")
        exit()
    table[i[1]][i[0]]=arr[i]

for j in range(total_st):
    for k in state[j]:
        if k[1][-1]==".":
            p=k[0] + k[1][:len(k[1]) - 1]
            if len(p)==1:
                p+="^"
                
            if p!="S'S":    
                ind=prod[p]
                for l in follow[p[0]]:
                    if table[l][j]!="_":
                        print("Ambiguous Grammar")
                        exit()
                    table[l][j]=-ind-1
                
table["$"][sp]="A"
print("\tTable \n")
# exit()
for i in table:
    print(i,"\t",*table[i],"\n")    

print("\tParsing\n")
s=(input())
s=s.replace(" ","")
s=list(s)
s+=["$"]
parse=["0"]
flag=0
try:
    while s:
        k=table[s[0]][int(parse[-1])]
        print(*parse,"\t\t\t",*s,)
        if k=="_":
            print("NOT ACCEPTED BY GRAMMAR")
            flag=1
            exit()
        elif k=="A":
            flag=1
            print("Accepted")
            exit(0)
        elif k>=0:    
            a=str(k)
            parse+=[s.pop(0)]
            parse+=[a]
        elif k<0:
            p=prod1[abs(k) - 1]
            if p[-1]=="^":
                p=p[:len(p)-1]
            for j in range(2*(len(p)-1)):
                parse.pop()
               
            parse+=[prod1[abs(k) - 1][0]]
            kk=table[prod1[abs(k) - 1][0]][int(parse[-2])]
            parse+=[kk]
    
except:
    if flag==0:
        print("NOT ACCEPTED BY GRAMMAR")
        flag=1
        exit()
if flag==0:
    print("NOT ACCEPTED BY GRAMMAR")
    exit()
