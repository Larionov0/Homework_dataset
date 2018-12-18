import re
import plotly
import plotly.graph_objs as go
from plotly import tools
def get_OMOID(line):
    result = re.split(r",",line,maxsplit=1)
    return result[0],result[1]
def get_OMONumber(line):
    result = re.split(r",",line,maxsplit=1)
    num = re.findall(r"[A-Z]\d{6}")
    return result[0],result[1]
def get_BuildingID(line):
    result = re.split(r",",line,maxsplit=1)
    return result[0],result[1]

dataset = dict()

def data_adder(dataset,OMOID,OMONumber,BuildingID,BoroID,Boro,HouseNumber,StreetName,Apartment,Zip):
    if Boro in dataset:
        if StreetName in dataset[Boro]:
            if BuildingID in dataset[Boro][StreetName]:
                print("")
            else:
                dataset[Boro][StreetName][BuildingID] = {
                                    "OMOID":OMOID,
                                    "OMONumber":OMONumber,
                                    "HouseNumber":HouseNumber,
                                    "Apartment":Apartment,
                                    "Zip":Zip
                                            }
        else:
            dataset[Boro][StreetName] = {
                                BuildingID:{
                                    "OMOID":OMOID,
                                    "OMONumber":OMONumber,
                                    "HouseNumber":HouseNumber,
                                    "Apartment":Apartment,
                                    "Zip":Zip
                                            }
                                        }

    else:
        dataset[Boro] = {
            "BoroID" : BoroID,
            StreetName:{
                BuildingID:{
                    "OMOID":OMOID,
                    "OMONumber":OMONumber,
                    "HouseNumber":HouseNumber,
                    "Apartment":Apartment,
                    "Zip":Zip
                            }
                        }
                         }





try:

    with open("data/OMO2.csv",mode = "r",encoding="utf-8") as file:

        header = file.readline().rstrip()

        nice_header = [column.strip().upper() for column in header.split(",")]
        num = nice_header.index("BORO")
        print(num)
        #c = 0
        for line in file:
            #c+=1
            if not line.rstrip():
                continue
            #line = line.split(",")
            #print(line[num])

            OMOID, new_line = get_OMOID(line)
            OMONumber, new_line = get_BuildingID(new_line)
            BuildingID, new_line = get_BuildingID(new_line)
            BoroID, new_line = get_BuildingID(new_line)
            Boro, new_line = get_BuildingID(new_line)
            HouseNumber, new_line = get_BuildingID(new_line)
            StreetName, new_line = get_BuildingID(new_line)
            Apartment, new_line = get_BuildingID(new_line)
            Zip, new_line = get_BuildingID(new_line)

            #print(BoroID,Boro)
            data_adder(dataset,OMOID,OMONumber,BuildingID,BoroID,Boro,HouseNumber,StreetName,Apartment,Zip)
            #if c >6:
            #    break
    print(dataset)


except IOError as io_error:
    print("Error with file",io_error.errno,io_error.strerror)
except ValueError as v_error:
    print("Error in line",current_line)
x =[]
y =[]
print(x,y)
for state in dataset:
    count = 0
    for street in dataset[state]:
        if street!="BoroID":
            for build in street:
                count+=1
    y.append(count)
    x.append(state)
x1 = []
y1 = []
for state in dataset:
    for street in dataset[state]:
        count = 0
        if street != "BoroID":
            for build in dataset[state][street]:
                for mag in dataset[state][street][build]:
                    if mag == "OMOID":
                        count+=1
            x1.append(street)
            y1.append(count)

diagram1 = go.Bar(x = x,y = y,name="Number of buildings in state")
diagram2 = go.Bar(x =x1,y =y1,name="Number of markets in street")
diagram3 = go.Pie(labels = x,values = y,name="Number of buildings in state")
figure = tools.make_subplots(rows = 2,cols = 2)

figure.append_trace(diagram1,1,1)
figure.append_trace(diagram2,1,2)
figure.append_trace(diagram3,2,1)

plotly.offline.plot(figure,filename="f.html")