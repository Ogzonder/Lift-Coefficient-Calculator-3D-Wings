import requests
from bs4 import BeautifulSoup

def alpha0_calc(airfoil,reynolds_number):
        alpha_list =[]
        cl_list=[]
     
        global polar_data
        global r
        global min_positive_val
        global max_negative_val
        global index_min
        global index_max
        global alpha_negativecl
        global alpha_positivecl
        r = requests.get("http://airfoiltools.com/polar/details?polar=xf-{}-{}".format(airfoil,reynolds_number))
        soup = BeautifulSoup(r.content,"lxml") 
        polar_data_set = soup.find_all("td",attrs ={"class":"cell2"})
       
        for data in polar_data_set:    
            polar_data = data.find("pre").find(text=True)
            # print(polar_data)
        
        
        with open("polar_data.txt", "w") as a:
             a.write(polar_data)
             a.close()    
            
        with open("polar_data.txt", "r+") as f:
            # f.write(polar_data)
            lines= f.readlines()
            for line in lines[13::]:
                new_line_alpha = line.lstrip()[0:6]
                new_line_cl = line.lstrip()[8:16]
                alpha_list.append(float(new_line_alpha))
                cl_list.append(float(new_line_cl))
                # print(alpha_list)
                # print(cl_list)
            #f.truncate(0)
            f.close()
            
            
            # print(alpha_list)
            # print(cl_list)
            
        min_positive_val = min([num for num in cl_list if num>0])
        max_negative_val = max([num for num in cl_list if num<0])
        
        index_min = cl_list.index(min_positive_val)
        index_max = cl_list.index(max_negative_val)
            
        alpha_negativecl = alpha_list[index_max]
        alpha_positivecl = alpha_list[index_min]
            
        alpha0 =-1*(((max_negative_val/(max_negative_val-min_positive_val))*(alpha_negativecl-alpha_positivecl))-alpha_negativecl)
            
        return alpha0
    
def check_stall_risk(airfoil,reynolds_number):
        alpha_list =[]
        cl_list=[]
    
        global polar_data
        global r
        global min_positive_val
        global max_negative_val
        global index_min
        global index_max
        global alpha_negativecl
        global alpha_positivecl
        
        r = requests.get("http://airfoiltools.com/polar/details?polar=xf-{}-{}".format(airfoil,reynolds_number))
        soup = BeautifulSoup(r.content,"lxml") 
        polar_data_set = soup.find_all("td",attrs ={"class":"cell2"})
       
        for data in polar_data_set:    
            polar_data = data.find("pre").find(text=True)
            # print(polar_data)
        
        
        with open("polar_data.txt", "w") as a:
             a.write(polar_data)
             a.close()    
            
        with open("polar_data.txt", "r+") as f:
            # f.write(polar_data)
            lines= f.readlines()
            for line in lines[13::]:
                new_line_alpha = line.lstrip()[0:6]
                new_line_cl = line.lstrip()[8:16]
                alpha_list.append(float(new_line_alpha))
                cl_list.append(float(new_line_cl))
                # print(alpha_list)
                # print(cl_list)
            #f.truncate(0)
            f.close()
            
   
        max_positive_val = max([num for num in cl_list if num>0])
        min_negative_val = min([num for num in cl_list if num<0])
        index_positive = cl_list.index(max_positive_val)
        index_negative = cl_list.index(min_negative_val)
        alpha_positive_peak = alpha_list[index_positive]
        alpha_negative_peak = alpha_list[index_negative]
        return alpha_negative_peak,alpha_positive_peak
# test = alpha0_calc("naca4412-il",1_000_000)
# print(test)
