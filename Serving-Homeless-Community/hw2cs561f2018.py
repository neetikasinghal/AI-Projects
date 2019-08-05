import time

start = time.time()

class Applicant:
    def __init__(self, info):
        self.id = info[0:5]
        self.gender = info[5]
        self.age = int(info[6:9])
        if(info[9]=='Y'):
            self.pets = True
        else:
            self.pets=False

        if (info[10] == 'Y'):
            self.medical = True
        else:
            self.medical = False

        if (info[11] == 'Y'):
            self.car = True
        else:
            self.car = False

        if (info[12] == 'Y'):
            self.license = True
        else:
            self.license = False

        self.days = info[13:20]
        self.type = self.popType()
        self.resources = self.getResourcesCount()

    def getIntGender(self):
        if(self.gender=='F'):
            return 1
        return 0

    def popType(self):
        if(self.car and self.license and not(self.medical) and self.age>17 and self.gender=='F' and not(self.pets)) :
            return 'P'
        if(self.car and self.license and not(self.medical)):
            return 'SP'
        if(self.age>17 and self.gender=='F' and not(self.pets)):
            return 'LP'
        return 'N'

    def isLHSA(self):
        if(self.type=='L'):
            return True
        return False

    def isSPLA(self):
        if(self.type=='S'):
            return True
        return False

    def getType(self):
        return self.type

    def setType(self,type):
        self.type = type

    def getResourcesCount(self):
        sum=0
        for i in self.days:
            sum+=int(i)
        return sum

    def getDaysAsList(self):
        res =[]
        for i in self.days:
            res.append(int(i))
        return res

    def getInfo(self):
        print self.id
        print self.gender
        print self.age
        print self.pets
        print self.medical
        print self.car
        print self.license
        print self.type
        print self.days+'\n'

    def getAge(self):
        return self.id

    def getId(self):
        return self.id

class Spaces:
    def __init__(self, b,p):
        self.b = b
        self.p = p
        self.bedDays=[b, b, b, b, b, b, b];
        self.parkDays=[p, p, p, p, p, p, p];

    def addRes(self,candidate,type):
        if(type=="SPLA"):
            list=candidate.getDaysAsList();
            for i in range(7):
                self.parkDays[i]=self.parkDays[i]+list[i]
            return self.parkDays
        if (type == "LHSA"):
            list = candidate.getDaysAsList();
            for i in range(7):
                self.bedDays[i] = self.bedDays[i] + list[i]
            return self.bedDays

    def add(self,resource,type):
        res=[]
        if(type=="LHSA"):
            for i in range(7):
                res[i]=self.bedDays[i]+resource.bedDays
        else:
            for i in range(7):
                res[i]=self.parkDays[i]+resource.parkDays
        return res

    def remove_lhsa_final(self, list):
        for i in range(7):
            self.bedDays[i]=self.bedDays[i]-list[i]

    def remove_spla_final(self, list):
        for i in range(7):
            self.parkDays[i] = self.parkDays[i]-list[i]

    def is_valid_list(self, list):
        for i in range(7):
            if(list[i]<0):
                return False
        return True

    def remove_probable(self, list, type):
        res = []
        if(type=="SPLA"):
            for i in range(7):
                res.append(self.parkDays[i] - list[i])
        else:
            if(type=="LHSA"):
                for i in range(7):
                    res.append(self.bedDays[i] - list[i])
        return res

    def sum_efficiency(self, type):
        sum=0
        if(type=="LHSA"):
            for i in range(7):
                sum=sum+int(self.bedDays[i])
        else:
            for i in range(7):
                sum=sum+int(self.parkDays[i])
        return sum

    def compare_resources(self, resource, type):
        sumSelf=self.sum_efficiency(type)
        sumResource=resource.sum_efficiency(type)

        if(sumSelf > sumResource):
            return "true"
        if(sumSelf < sumResource):
            return "false"
        if(sumSelf==sumResource):
            return "equal"

class Default:
    spla_counter = []
    lahsa_counter = []

    def __init__(self, both_SL, only_S, only_L, b_list, p_list):
        self.bothSL=both_SL
        self.onlyS=only_S
        self.onlyL=only_L
        self.spla_list=self.create_desired_list(only_S)
        self.lahsa_list=self.create_desired_list(only_L)
        self.spla_lahsa_list=self.create_desired_list(both_SL)
        self.spla_counter = p_list
        self.lahsa_counter = b_list


    def create_desired_list(self, lis):
        res=[]
        for x in lis:
            res.append([x.getId(),x.days])
        return res

    def greedy_fn(self, spla_list, lahsa_list, spla_lahsa_list):
        # sort the eligibility lists by requested number of days
        spla_list.sort(key=return_max, reverse=True)
        lahsa_list.sort(key=return_max, reverse=True)
        spla_lahsa_list.sort(key=return_max, reverse=True)
        # initialize the chosen applicants lists
        spla_chosen_appl = []
        lahsa_chosen_appl = []
        flag = 1
        for i in range(len(spla_lahsa_list)):
            if (i % 2 == 0):
                if (evaluate_space(self.spla_counter, str(spla_lahsa_list[i][1])) != -1):
                    spla_chosen_appl.append(spla_lahsa_list[i][0])
                else:
                    flag = 0
                    break
            else:
                if (evaluate_space(self.lahsa_counter, str(spla_lahsa_list[i][1])) != -1):
                    lahsa_chosen_appl.append(spla_lahsa_list[i][0])
                else:
                    #print("Warning: Applicants left but space empty")
                    flag = 0
                    break

        if (flag):
            for i in range(len(spla_list)):
                if (evaluate_space(self.spla_counter, str(spla_list[i][1])) != -1):
                    spla_chosen_appl.append(spla_list[i][0])
                else:
                    flag = 0
                    break
        if (flag):
            for i in range(len(lahsa_list)):
                if (evaluate_space(self.lahsa_counter, str(lahsa_list[i][1])) != -1):
                    spla_chosen_appl.append(lahsa_list[i][0])
                else:
                    flag = 0
                    break
        # choose the first applicant from the respective list if all applicants can be accommodated
        if not spla_lahsa_list and not spla_list:
            return "00000"
        elif not spla_lahsa_list:
            return spla_list[0][0]
        else:
            return spla_lahsa_list[0][0]

#check if the applicant can be accommodated
def evaluate_space(g_counter,req):
   temp=[]*7
   count, flag=0, 0
   for i in req:
       temp.append(g_counter[count] - int(i))
       if temp[count]==-1:
           flag=1;
           break;
       count+=1

   if (flag == 1):
       return -1
   else:
       g_counter[:]=list(temp)
       return 0

def return_max(sort_list):
    n = int(sort_list[1])
    r = 0
    while n:
        r, n = r + n % 10, n // 10
    return r

def check_time():
    period_of_time = 176
    if time.time() > start + period_of_time:
        return True
    return False

def get_both_probable_candidates(candidateList):
    probCan = []
    for x in candidateList:
        if(x.getType()=='P'):
            probCan.append(x)
    return probCan

def get_only_probabale_sorted_candidates(candidateList, param):
    probCan=[]
    for x in candidateList:
        if(x.getType()==param):
            probCan.append(x)
    return sort_resources(probCan)

def populate_type(list, cType, candidateList):
    for x in range(len(list)):
        candidateList[int(list[x])-1].setType(cType)

def is_valid(resType, resource, candidate, type):
    check=resType.is_valid_list(resource.remove_probable(resType.addRes(candidate, type), type))
    if(check==False):
        resType.bedDays=resType.remove_probable(candidate.getDaysAsList(), type)
        return check
    else:
        return check

def is_simple_valid(resource, candidate, type):
    return resource.is_valid_list(resource.remove_probable(candidate.getDaysAsList(), type))

def sort_resources_gender(probCan):
    return sorted(probCan,key=lambda candidate: (candidate.getIntGender(), candidate.resources), reverse=True)

def sort_resources(list):
    return sorted(list,key=lambda candidate: candidate.resources, reverse=True)

def get_only_required_resources(resType, resource, list, type):
    res=[]
    for x in list:
        if resType.is_valid_list(resource.remove_probable(resType.addRes(x, type), type)):
            res.append(x)
        else:
            resType.remove_probable(x.getDaysAsList(), type)
    return res

def validate_lahsa(lis, candidate):
    for i in range(len(lis)):
        if(lis[i].getId()==candidate.getId()):
            return False
    return True

def calculate_efficiency(rc, r_count, type):
    if(type=="SPLA"):
        if(r_count.p==0):
            r_count.p = rc.p
            r_count.b = rc.b
        if(rc.p>r_count.p):
            r_count.p = rc.p
            r_count.b = rc.b
    else:
        if(r_count.b==0):
            r_count.b = rc.b
            r_count.p = rc.p
        if(rc.b>r_count.b):
            r_count.b = rc.b
            r_count.p = rc.p

def lahsa_dfs(lhsa_res, spla_res, l, l_list, resource, candidate_list, max_res, r_count):
    if check_time():
        return
    if(len(l_list)==l):
        if(r_count.b<lhsa_res.sum_efficiency("LHSA")):
            r_count.p=spla_res.sum_efficiency("SPLA")
            r_count.b=lhsa_res.sum_efficiency("LHSA")

        r = lhsa_res.compare_resources(max_res, "LHSA")
        if r == "equal" or r == "true":
            for i in range(7):
                max_res.bedDays[i] = lhsa_res.bedDays[i]
        return

    for i in range(l, len(l_list)):
        if (is_valid(lhsa_res, resource, l_list[i], "LHSA")):
            lahsa_dfs(lhsa_res, spla_res, i + 1, l_list, resource, candidate_list, max_res, r_count)
            lhsa_res.bedDays = lhsa_res.remove_probable(l_list[i].getDaysAsList(), "LHSA")

def spla_dfs(lhsa_res, spla_res, s, s_list, resource, candidate_list, max_res, r_count):
    if check_time():
        return
    if(len(s_list)==s):
        if(r_count.p<spla_res.sum_efficiency("SPLA")):
            r_count.p=spla_res.sum_efficiency("SPLA")
            r_count.b=lhsa_res.sum_efficiency("LHSA")

        r = spla_res.compare_resources(max_res, "SPLA")
        if r == "equal" or r == "true":
            for i in range(7):
                max_res.parkDays[i] = spla_res.parkDays[i]
        return

    for i in range(s, len(s_list)):
        if (is_valid(spla_res, resource, s_list[i], "SPLA")):
            spla_dfs(lhsa_res, spla_res, i + 1, s_list, resource, candidate_list, max_res, r_count)
            spla_res.parkDays = spla_res.remove_probable(s_list[i].getDaysAsList(), "SPLA")

def get_all_validate_candidates(fullList, lis):
    return [x for x in fullList if x not in lis]

def DFS(spla_res, lahsa_res, s, l, spla_list, lahsa_list, resource, candidate_list, max_res, s_lis, l_lis, flag, r_count):
    if check_time():
        return
    if (not flag):
        # LAHSA
        res = get_all_validate_candidates(get_all_validate_candidates(lahsa_list, s_lis), l_lis)
        check = True
        for i in range(len(res)):
            if is_valid(lahsa_res, resource, res[i], "LHSA"):
                check = False
                l_lis.append(res[i])
                rC = Spaces(0, 0)
                DFS(spla_res, lahsa_res, s, l, spla_list, lahsa_list, resource, candidate_list, max_res, s_lis, l_lis,
                    not flag, rC)
                calculate_efficiency(rC, r_count, "LHSA")
                l_lis.remove(res[i])
                lahsa_res.bedDays = lahsa_res.remove_probable(res[i].getDaysAsList(), "LHSA")
        if (check):
            spla_dfs(lahsa_res, spla_res, 0,
                     get_all_validate_candidates(get_all_validate_candidates(spla_list, s_lis), l_lis), resource,
                     candidate_list, max_res, r_count)
        return

    if(flag):
        # SPLA
        res = get_all_validate_candidates(get_all_validate_candidates(spla_list, l_lis), s_lis)
        check=True
        for i in range(len(res)):
            if is_valid(spla_res, resource, res[i], "SPLA"):
                check= not check
                s_lis.append(res[i])
                rC=Spaces(0, 0)
                DFS(spla_res, lahsa_res, s, l, spla_list, lahsa_list, resource, candidate_list, max_res, s_lis, l_lis, not flag, rC)
                calculate_efficiency(rC, r_count, "SPLA")
                s_lis.remove(res[i])
                spla_res.parkDays = spla_res.remove_probable(res[i].getDaysAsList(), "SPLA")
        if(check):
            lahsa_dfs(lahsa_res, spla_res, 0, get_all_validate_candidates(get_all_validate_candidates(lahsa_list, l_lis), s_lis), resource, candidate_list, max_res, r_count)
        return

def run(resource, candidateList, check):
    prob_can = get_both_probable_candidates(candidateList)
    prob_can = sort_resources_gender(prob_can)

    spla_probable_list = get_only_probabale_sorted_candidates(candidateList, "SP")
    lhsa_probable_list = get_only_probabale_sorted_candidates(candidateList, "LP")

    greedy = Default(prob_can, spla_probable_list, lhsa_probable_list, list(resource.bedDays), list(resource.parkDays))
    greedy_ans=greedy.greedy_fn(greedy.spla_list, greedy.lahsa_list, greedy.spla_lahsa_list)

    s_list = prob_can+spla_probable_list
    s_list = sort_resources(s_list)
    l_list = prob_can+lhsa_probable_list
    l_list = sort_resources(l_list)

    res_max = Spaces(0, 0)
    result = Applicant(str(greedy_ans) + "O000YYNN0000000")
    for i in range(len(s_list)):
        spla_res = Spaces(0, 0)
        lhsa_res = Spaces(0, 0)
        if (is_valid(spla_res, resource, s_list[i], "SPLA")):
            res = Spaces(0, 0)
            rCount=Spaces(0, 0)
            sLis=[]
            lLis=[]
            sLis.append(s_list[i])
            turn=False
            DFS(spla_res, lhsa_res, i + 1, 0, s_list, l_list, resource, candidateList, res, sLis, lLis, turn, rCount)
            if(rCount.p==res_max.p):
                if(rCount.b==res_max.b):
                    if(result.resources==s_list[i].resources):
                        if(int(result.getId())>int(s_list[i].getId())):
                            result=s_list[i]
                    if(result.resources<s_list[i].resources):
                        result=s_list[i]
                if(rCount.b>res_max.b):
                    result=s_list[i]
                    res_max.b=rCount.b
            if(rCount.p>res_max.p):
                result=s_list[i]
                res_max.p=rCount.p
                res_max.b=rCount.b
            spla_res.parkDays = spla_res.remove_probable(s_list[i].getDaysAsList(), "SPLA")
        if check_time():
            return result
    return result


if __name__ == '__main__':
    fin = open('input.txt', 'r')
    fout = open('output.txt', 'w')

    bed_spaces = int(fin.readline())
    parking_spaces = int(fin.readline())
    efficiency = Spaces(bed_spaces, parking_spaces)

    lahsa_applicants = int(fin.readline())
    lahsa_list = []
    for i in range(lahsa_applicants):
        lahsa_list.append(str(fin.readline()))

    spla_applicants = int(fin.readline())
    spla_list = []
    for i in range(spla_applicants):
        spla_list.append(str(fin.readline()))

    total_applicants = int(fin.readline())
    candidate_list = []
    for i in range(total_applicants):
        candidate_list.append(Applicant(fin.readline()))

    check=False
    if total_applicants <= parking_spaces:
        check = True

    populate_type(lahsa_list, 'L', candidate_list)
    populate_type(spla_list, 'S', candidate_list)

    for i in spla_list:
        efficiency.remove_spla_final(candidate_list[int(i) - 1].getDaysAsList())

    for i in lahsa_list:
        efficiency.remove_lhsa_final(candidate_list[int(i) - 1].getDaysAsList())

    fout.write(run(efficiency, candidate_list, check).getId())
    fout.close()
    fin.close()