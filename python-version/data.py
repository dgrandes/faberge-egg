

def extractDataFromInputFile(i):
    data = []

    with open(i) as f:
        reader = csv.reader(f)
        
        for row in reader:
            #Regex to match all the zeroes only numbers and make them None
            zeroes = re.search("^0000+", row[1])

            if row[1] == '' or row[1] == '0' or row[1] == '0700000000' or zeroes: 
                row[1] = None
            if row[0] == '':
                row[0] = None
            if row[0] != "email":
                data.append((row[0],row[1]))
            
    return data

def printUsersData(users, printB2C = True, printC2C = False):
    #Users with more than one email and phone
    b2cUsers = dict((k, v) for k, v in users.items() if len(v) > 2)
    c2cUsers = dict((k, v) for k, v in users.items() if len(v) <= 2)
    print "Amount of Users in Total: ",len(users)
    print "Amount of Users with more than one Email and Phone: ", len(b2cUsers)
    if printC2C:
        print "\n"
        print "C2C Users Detail: \n"
        pp.pprint(c2cUsers)
    if printB2C:
        print "\n"
        print "B2C Users Detail: \n"
        pp.pprint(b2cUsers)

def outputDataToFile(users, output, scenario, displayProgressEnabled=True):
    csv_writer_emails = csv.writer(open(output+"_Emails.csv", "wt"), quoting=csv.QUOTE_ALL) # create csv
    csv_writer_phones = csv.writer(open(output+"_Phones.csv", "wt"), quoting=csv.QUOTE_ALL) # create csv
    csv_writer_users = csv.writer(open(output+"_Users.csv", "wt"), quoting=csv.QUOTE_ALL) # create csv
    csv_writer_users.writerow(("scenario", "metauserid", "# emails", "# phones"))
    csv_writer_phones.writerow(("scenario", "metauserid", "phone"))
    csv_writer_emails.writerow(("scenario", "metauserid", "emails"))

    iterableUsers = users
    if displayProgressEnabled:
        pbar = ProgressBar()
        iterableUsers = pbar(users)
    for i in iterableUsers:
        emails = [v for v in users[i] if "@" in v]
        phones = [v for v in users[i] if  not "@" in v and v is not None and v != ""]
        csv_writer_users.writerow((scenario, i,len(emails),len(phones)))
        for p in phones:
            csv_writer_phones.writerow((scenario, i, p))
        for e in emails:
            csv_writer_emails.writerow((scenario, i, e))    
    
    # close csv files
    del csv_writer_emails 
    del csv_writer_phones 
    del csv_writer_users

    
