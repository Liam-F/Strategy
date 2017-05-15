# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 12:47:04 2015

@author: jlinot

This file enables to create and use US Calendars 

"""

#*****************************************************************************
#                           IMPORTS
#*****************************************************************************

#*************************
# IMPORT PYTHON LIBRAIRIES
#*************************

import datetime
from calendar import monthrange

class Date :
    @staticmethod
    def lastOccurenceOfDayOfMonth(dayOfWeek, month, year):
        tmp = datetime.datetime(year = year, month = month, day = monthrange(year,month)[1])
        while (tmp.weekday() != dayOfWeek):
            tmp = tmp + datetime.timedelta(days = -1)
        
        return tmp
    
    
    @staticmethod
    def occurenceOfDayOfMonth(numOccurence, dayOfWeek, month, year):
        tmp = datetime.datetime(year = year, month = month, day = 1)
        count = 0
        if (tmp.weekday() == dayOfWeek):
            count += 1
        
        while(count != numOccurence):
            tmp = tmp + datetime.timedelta(days = 1)
            if (tmp.weekday() == dayOfWeek):
                count += 1
        
        return tmp

class Calendar :

    def __init__(self, startDate, endDate):
        self.start=startDate
        self.end = endDate
        self.AllFixingDates = self.generateAllFixingDates()
        self.AllButWeekendFixingDates = self.generateAllButWeekendFixingDates()
        self.BusinessDaysFixingDates = self.generateBusinessDaysFixingDates()
    
    def specialUSMarketHolidayRule(self,date):
        if (date.weekday() == 6):
            return (date + datetime.timedelta(days = 1))
        elif (date.weekday() == 5):
            return (date + datetime.timedelta(days = -1))
        else:
            return date
    
    def specialPastHoliday(self,year, month, day):
        if (year == 1985 and month == 9 and day == 27):
            return True
        elif (year == 1994 and month == 4 and day == 27):
            return True
        elif (year == 2001 and month == 9 and day == 11):
            return True
        elif (year == 2001 and month == 9 and day == 12):
            return True
        elif (year == 2001 and month == 9 and day == 13):
            return True
        elif (year == 2001 and month == 9 and day == 14):
            return True
        elif (year == 2004 and month == 6 and day == 11):
            return True
        elif (year == 2007 and month == 1 and day == 2):
            return True
        elif (year == 2012 and month == 10 and day == 29):
            return True
        elif (year == 2012 and month == 10 and day == 30):
            return True
        else:
            return False
           
    def easterSunday(self,year):
        g = year % 19
        c = int(year / 100)
        h = (c - (int)(c / 4) - (int)((8 * c + 13) / 25) + 19 * g + 15) % 30
        i = h - (int)(h / 28) * (1 - (int)(h / 28) * (int)(29 / (h + 1)) * (int)((21 - g) / 11))
        day = i - ((year + (int)(year / 4) + i + 2 - c + (int)(c / 4)) % 7) + 28
        month = 3
        
        if (day > 31):
            month += 1
            day -= 31
        
        return datetime.datetime(year = year, month = month, day = day)
           
           
    def goodFriday(self,year):
        return (self.easterSunday(year) + datetime.timedelta(days = -2))
    
           
    def isHoliday(self,date):
        if ((date.day == 25 and date.month == 12) or (self.specialUSMarketHolidayRule(datetime.datetime(year = date.year, month = 12, day = 25)) == date )):
            return True
        elif ((date.day == 4 and date.month == 7) or (self.specialUSMarketHolidayRule(datetime.datetime(year=date.year,month = 7, day = 4)) == date)):
            return True
        elif ((date.day == 1 and date.month == 1) or (self.specialUSMarketHolidayRule(datetime.datetime(year=date.year,month = 1, day = 1)) == date)):
            return True
        elif (Date.occurenceOfDayOfMonth(1,0,9,date.year) == date):
            return True
        elif (Date.occurenceOfDayOfMonth(3,0,1,date.year) == date):
            return True
        elif (Date.occurenceOfDayOfMonth(4,3,11,date.year) == date):
            return True
        elif (Date.occurenceOfDayOfMonth(3,0,2,date.year) == date):
            return True
        elif (Date.lastOccurenceOfDayOfMonth(0,5,date.year) == date):
            return True
        elif (self.goodFriday(date.year) == date):
            return True
        elif (self.specialPastHoliday(date.year, date.month, date.day)):
            return True
        else:
            return False
    
    def isWeekend(self,date):
        if (date.weekday() == 5 or date.weekday() == 6 ):
            return True
        else:
            return False
    
    def isBusinessDay(self,date):
        if(self.isWeekend(date) or self.isHoliday(date)):
            return False
        else:
            return True
    
    def nextBusinessDay(self,date):
        tmp = date + datetime.timedelta(days=1)
        while (self.isBusinessDay(tmp) != True):
            tmp = tmp + datetime.timedelta(days = 1)
        
        return tmp
        
    def generateAllFixingDates(self):
        res = []
        tmp = self.start
        while(tmp <= self.end):
            res.append(tmp)
            tmp = tmp + datetime.timedelta(days = 1)
        
        return res
    
    def generateAllButWeekendFixingDates(self):
        res = []
        tmp = self.start

        if (self.isWeekend(tmp) == True):
            tmp = self.nextBusinessDay(self.start)       
        
        while(tmp <= self.end):
            res.append(tmp)            
            tmp = tmp + datetime.timedelta(days = 1)
            while (self.isWeekend(tmp)):
                tmp = tmp + datetime.timedelta(days = 1)
                
        return res
    
    
    def generateBusinessDaysFixingDates(self):
        res = []
        tmp = self.start
        
        if (self.isBusinessDay(tmp) != True):
            tmp = self.nextBusinessDay(self.start)     
    
        while(tmp <= self.end):
            res.append(tmp)
            tmp = tmp + datetime.timedelta(days = 1)
            while (self.isBusinessDay(tmp) != True):
                tmp = tmp + datetime.timedelta(days = 1)
    
        return res
    
    def addBusinessDays(self,nbOfDays,date):
        tmp = date
        count = 0
        if (nbOfDays >=0):
            while (count < nbOfDays):
                tmp = tmp + datetime.timedelta(days=1)
                if (self.isBusinessDay(tmp)):
                    count += 1
        else:
            while (count > nbOfDays):
                tmp = tmp + datetime.timedelta(days=-1)
                if (self.isBusinessDay(tmp)):
                    count -= 1
        
        return tmp
        
    def nbBusinessDaysBetweenTwoDates_exact(self,date1,date2):
        if (date1 > date2):
            raise ValueError("date1 should be before date2")
            
        count = 0
        tmp = date1
        
        while (tmp <date2):
            tmp = self.addBusinessDays(1,tmp)
            count += 1
    
        return count   
        
        
        
    def nbBusinessDaysBetweenTwoDates(self,date1,date2):
        if (date1 > date2):
            raise ValueError("date1 should be before date2")
            
        count = 0
        tmp = date1
        
        while (tmp <= date2):
            tmp = self.addBusinessDays(1,tmp)
            count += 1
    
        return count
    
    def nbBusinessDaysBetweenTwoDates_Period(self,date1,date2):
        if (date1 > date2):
            raise ValueError("date1 should be before date2")
            
        count = 0
        tmp = date1
        tmp = self.addBusinessDays(1,tmp)
        while (tmp <= date2):
            tmp = self.addBusinessDays(1,tmp)
            count += 1
    
        return count
        
    def nbBusinessDaysBetweenTwoDates_Remaining(self,date1,date2):
        if (date1 > date2):
            raise ValueError("date1 should be before date2")
            
        count = 0
        tmp = date1
        tmp = self.addBusinessDays(1,tmp)
        while (tmp <= date2):
            tmp = self.addBusinessDays(1,tmp)
            count += 1
    
        return count
        
    def MonthFirstBusinessDay(self,date):
        month=date.month
        year =date.year
        day = 1
        date = datetime.datetime(year,month,day)
        
        while self.isBusinessDay(date)==False:
            day+=1
            date = datetime.datetime(year,month,day)
        return date
    
    def MonthLastBusinessDay(self,date):
        month=date.month
        year =date.year
        if month ==12:
            month = 1
            year+=1
        else:
            month +=1 
        day = 1
        date = datetime.datetime(year,month,day)
        date = date+ datetime.timedelta(days=-1)
        while not self.isBusinessDay(date) :
            date = date+ datetime.timedelta(days=-1)
        
        while self.isBusinessDay(date)==False:
            day+=1
            date = datetime.datetime(year,month,day)
        return date
        
    def check_date(year, month, day):
        correctDate = None
        try:
            newDate = datetime.datetime(year, month, day)
            correctDate = True
        except ValueError:
            correctDate = False
        return correctDate