import sqlite3

connection=sqlite3.connect("College_Student.db")

cursor = connection.cursor()

table_info = """create table College_Student(ID INT,Name VARCHAR(20),Age INT,Gender CHAR,Department VARCHAR(20),CGPA FLOAT)"""

cursor.execute(table_info)

"insert data"

cursor.execute('''INSERT INTO College_Student VALUES(1,'Aarav',19,'M','CSE',6.37),
                                                    (2,'Aditi',20,'F','IT',6.74),
                                                    (3,'Rahul',21,'M','ECE',7.11),
                                                    (4,'Sneha',22,'F','ME',7.48),
                                                    (5,'Rohan',23,'M','CIVIL',7.85),
                                                    (6,'Priya',18,'F','CSE',8.22),
                                                    (7,'Karan',19,'M','IT',8.59),
                                                    (8,'Neha',20,'F','ECE',8.96),
                                                    (9,'Vikas',21,'M','ME',9.33),
                                                    (10,'Anjali',22,'F','CIVIL',9.70),
                                                    (11,'Mohit',23,'M','CSE',6.11),
                                                    (12,'Pooja',18,'F','IT',6.48),
                                                    (13,'Arjun',19,'M','ECE',6.85),
                                                    (14,'Kavya',20,'F','ME',7.22),
                                                    (15,'Deepak',21,'M','CIVIL',7.59),
                                                    (16,'Ritika',22,'F','CSE',7.96),
                                                    (17,'Yash',23,'M','IT',8.33),
                                                    (18,'Simran',18,'F','ECE',8.70),
                                                    (19,'Nikhil',19,'M','ME',9.07),
                                                    (20,'Isha',20,'F','CIVIL',9.44),
                                                    (21,'Ritesh',21,'M','CSE',9.81),
                                                    (22,'Anu',22,'F','IT',6.22),
                                                    (23,'Sachin',23,'M','ECE',6.59),
                                                    (24,'Megha',18,'F','ME',6.96),
                                                    (25,'Abhishek',19,'M','CIVIL',7.33),
                                                    (26,'Divya',20,'F','CSE',7.70),
                                                    (27,'Harsh',21,'M','IT',8.07),
                                                    (28,'Payal',22,'F','ECE',8.44),
                                                    (29,'Aman',23,'M','ME',8.81),
                                                    (30,'Nisha',18,'F','CIVIL',9.18),
                                                    (31,'Ravi',19,'M','CSE',9.55),
                                                    (32,'Komal',20,'F','IT',9.92),
                                                    (33,'Sandeep',21,'M','ECE',6.33),
                                                    (34,'Shreya',22,'F','ME',6.70),
                                                    (35,'Ajay',23,'M','CIVIL',7.07),
                                                    (36,'Muskan',18,'F','CSE',7.44),
                                                    (37,'Rakesh',19,'M','IT',7.81),
                                                    (38,'Tina',20,'F','ECE',8.18),
                                                    (39,'Manish',21,'M','ME',8.55),
                                                    (40,'Rekha',22,'F','CIVIL',8.92),
                                                    (41,'Aakash',23,'M','CSE',9.29),
                                                    (42,'Sonia',18,'F','IT',9.66),
                                                    (43,'Tarun',19,'M','ECE',6.07),
                                                    (44,'Jyoti',20,'F','ME',6.44),
                                                    (45,'Lokesh',21,'M','CIVIL',6.81),
                                                    (46,'Pallavi',22,'F','CSE',7.18),
                                                    (47,'Vinay',23,'M','IT',7.55),
                                                    (48,'Monika',18,'F','ECE',7.92),
                                                    (49,'Ashish',19,'M','ME',8.29),
                                                    (50,'Swati',20,'F','CIVIL',8.66),
                                                    (51,'Hemant',21,'M','CSE',9.03),
                                                    (52,'Khushi',22,'F','IT',9.40),
                                                    (53,'Gaurav',23,'M','ECE',9.77),
                                                    (54,'Ruchi',18,'F','ME',6.18),
                                                    (55,'Shubham',19,'M','CIVIL',6.55),
                                                    (56,'Aisha',20,'F','CSE',6.92),
                                                    (57,'Nitin',21,'M','IT',7.29),
                                                    (58,'Sakshi',22,'F','ECE',7.66),
                                                    (59,'Prashant',23,'M','ME',8.03),
                                                    (60,'Mansi',18,'F','CIVIL',8.40),
                                                    (61,'Adarsh',19,'M','CSE',8.77),
                                                    (62,'Anita',20,'F','IT',9.14),
                                                    (63,'Bhavesh',21,'M','ECE',9.51),
                                                    (64,'Rupal',22,'F','ME',9.88),
                                                    (65,'Chirag',23,'M','CIVIL',6.29),
                                                    (66,'Pallak',18,'F','CSE',6.66),
                                                    (67,'Dheeraj',19,'M','IT',7.03),
                                                    (68,'Suhani',20,'F','ECE',7.40),
                                                    (69,'Farhan',21,'M','ME',7.77),
                                                    (70,'Kriti',22,'F','CIVIL',8.14),
                                                    (71,'Gopal',23,'M','CSE',8.51),
                                                    (72,'Heena',18,'F','IT',8.88),
                                                    (73,'Imran',19,'M','ECE',9.25),
                                                    (74,'Jiya',20,'F','ME',9.62),
                                                    (75,'Kishan',21,'M','CIVIL',6.03),
                                                    (76,'Lata',22,'F','CSE',6.40),
                                                    (77,'Madan',23,'M','IT',6.77),
                                                    (78,'Nandini',18,'F','ECE',7.14),
                                                    (79,'Om',19,'M','ME',7.51),
                                                    (80,'Preeti',20,'F','CIVIL',7.88),
                                                    (81,'Qasim',21,'M','CSE',8.25),
                                                    (82,'Rani',22,'F','IT',8.62),
                                                    (83,'Shivam',23,'M','ECE',8.99),
                                                    (84,'Tanvi',18,'F','ME',9.36),
                                                    (85,'Umesh',19,'M','CIVIL',9.73),
                                                    (86,'Vaishali',20,'F','CSE',6.14),
                                                    (87,'Wasim',21,'M','IT',6.51),
                                                    (88,'Xena',22,'F','ECE',6.88),
                                                    (89,'Yogesh',23,'M','ME',7.25),
                                                    (90,'Zoya',18,'F','CIVIL',7.62),
                                                    (91,'Akhil',19,'M','CSE',7.99),
                                                    (92,'Bhavna',20,'F','IT',8.36),
                                                    (93,'Chetan',21,'M','ECE',8.73),
                                                    (94,'Diksha',22,'F','ME',9.10),
                                                    (95,'Eshan',23,'M','CIVIL',9.47),
                                                    (96,'Falguni',18,'F','CSE',9.84),
                                                    (97,'Ganesh',19,'M','IT',6.25),
                                                    (98,'Himani',20,'F','ECE',6.62),
                                                    (99,'Rohit',21,'M','ME',6.99),
                                                    (100,'Janvi',22,'F','CIVIL',7.36)''')


print('The inserted data records are')

data = cursor.execute('''select * from College_Student''')

for row in data:
    print(row)

#Commit your changes int he databse
connection.commit()
connection.close()