from ontology import *

class SimpleStatistics:
    def getCountEntitiesForClass(ontology, className):
        classes=ontology.getAllClasses()
        if(not className in classes):
            raise Exception('error in getCountEntitiesForClass in SimpleStatistics: class "'+className+'" does exist in this ontology')
        return len(ontology.getAllEntitiesForClass(className))
    
    def getMaxCountEntitiesForAnyClass(ontology):
        classes=ontology.getAllClasses()
        maxCount=0
        for className in classes:
            maxCount=max(maxCount,len(ontology.getAllEntitiesForClass(className)))
        return maxCount
    
    def getEmptyClasses(ontology):
        classes=ontology.getAllClasses()
        emptyClasses=[]
        for className in classes:
            if(len(ontology.getAllEntitiesForClass(className))==0):
                emptyClasses.append(className)
        return emptyClasses
    
    def getCountEntitiesForClassWhitchSatisfyRelationships(ontology, className, withRelationships, withoutRelationships):
        return len(SimpleStatistics.getEntitiesForClassWhitchSatisfyRelationships(ontology, className, withRelationships, withoutRelationships))
    
    def getEntitiesForClassWhitchSatisfyRelationships(ontology, className, withRelationships, withoutRelationships):
        classes=ontology.getAllClasses()
        if(not className in classes):
            raise Exception('error in getEntitiesForClassWhitchSatisfyRelationships in SimpleStatistics: class "'+className+'" does exist in this ontology')
        
        existingRelationships=set(ontology.getAllRelationshipsForOutClass(className))
        if(not(withRelationships<=existingRelationships) or not(withoutRelationships<=existingRelationships)):
            raise Exception('error in getEntitiesForClassWhitchSatisfyRelationships in SimpleStatistics: at least 1 of used relationships for a constraint does not esists in this ontology')
        
        res=[]
        for entity_ in ontology.getAllEntitiesForClass(className):
            relationships=set([i[2] for i in ontology.getAllRelationshipedEntitiesForOutEntity(entity_, className)])
            if(len(relationships&withoutRelationships)==0 and (withRelationships<=relationships)):
                res.append(entity_)
        return res
    
    def getAverageLinkBetweenClassesFor(ontology, outClassName, inClassName, forInClass = False):
        specifiedRelationships=set(ontology.getAllRelationshipsForOutClass(outClassName))
        return SimpleStatistics.getAverageLinkBetweenClassesForSpecifiedRelationshipsWhitchSatisfyRelationships(\
            ontology, outClassName, inClassName, specifiedRelationships, set(), set(), forInClass\
        )
    
    def getAverageLinkBetweenClassesWhitchSatisfyRelationships(ontology, outClassName, inClassName, withRelationships, withoutRelationships, forInClass = False):
        specifiedRelationships=set(ontology.getAllRelationshipsForOutClass(outClassName))
        return SimpleStatistics.getAverageLinkBetweenClassesForSpecifiedRelationshipsWhitchSatisfyRelationships(\
            ontology, outClassName, inClassName, specifiedRelationships, withRelationships, withoutRelationships, forInClass\
        )
        
    def getAverageLinkBetweenClassesForSpecifiedRelationships(ontology, outClassName, inClassName, specifiedRelationships, forInClass = False):
        return SimpleStatistics.getAverageLinkBetweenClassesForSpecifiedRelationshipsWhitchSatisfyRelationships(\
            ontology, outClassName, inClassName, specifiedRelationships, set(), set(), forInClass\
        )
        
    def getAverageLinkBetweenClassesForSpecifiedRelationshipsWhitchSatisfyRelationships(\
        ontology, outClassName, inClassName, specifiedRelationships, withRelationships, withoutRelationships, forInClass = False):
        classes=ontology.getAllClasses()
        if(not inClassName in classes):
            raise Exception('error in getAverageLinkBetweenClassesForSpecifiedRelationshipsWhitchSatisfyRelationships or similar in SimpleStatistics: an in class "'+\
                inClassName+'" does exist in this ontology')
        if(not outClassName in classes):
            raise Exception('error in getAverageLinkBetweenClassesForSpecifiedRelationshipsWhitchSatisfyRelationships or similar in SimpleStatistics: an out class "'+\
                outClassName+'" does exist in this ontology')
        
        existingRelationships=set(ontology.getAllRelationshipsForOutClass(outClassName))
        if(not(withRelationships<=existingRelationships) or not(withoutRelationships<=existingRelationships) or not(specifiedRelationships<=existingRelationships)):
            raise Exception('error in getAverageLinkBetweenClassesForSpecifiedRelationshipsWhitchSatisfyRelationships or similar in SimpleStatistics: '+\
                'at least 1 of used relationships for a constraint does not esists in this ontology')
        
        links=0
        for entity_ in ontology.getAllEntitiesForClass(outClassName):
            relationshipsWithClasses=ontology.getAllRelationshipedEntitiesForOutEntity(entity_, outClassName)
            
            relationships=[i[2] for i in relationshipsWithClasses]
            if(not(len(set(relationships)&withoutRelationships)==0 and (withRelationships<=set(relationships)))):
                continue
            
            relationships=[i[2] for i in relationshipsWithClasses if i[0]==inClassName]
            links+=len([i for i in relationships if i in specifiedRelationships])
        if(forInClass):
            return links/SimpleStatistics.getCountEntitiesForClass(ontology, inClassName)
        else:
            return links/SimpleStatistics.getCountEntitiesForClass(ontology, outClassName)
