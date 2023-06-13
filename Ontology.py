import pickle

class Ontology:
    class Class:
        class Relationship:
            name=''
            inClassName=''
            def __init__(self,name,inClassName):
                self.name=name
                self.inClassName=inClassName
        class Entity:
            class EntityRelationship:
                name=''
                inClassName=''
                inEntityName=''
                def __init__(self,name,inClassName,inEntityName):
                    self.name=name
                    self.inClassName=inClassName
                    self.inEntityName=inEntityName    
            name=''
            entityRelationships=[]
            
            def __init__(self,name):
                self.name=name
                self.entityRelationships=[]
        
        name=''
        relationships=[]
        entities=[]
        
        def __init__(self,name):
            self.name=name
            self.entities=[]
            self.relationshops=[]
    
    ontology=[]
    
    def __init__(self,fileName=None):
        if(not fileName==None):
            self.loadFromFile(fileName)
    
    def addClass(self,className):
        if(className in [i.name for i in self.ontology]):
            raise Exeption('error in addClass in Ontology: this class name "' + className + '" already exists in this ontology')
        
        self.ontology.append(Ontology.Class(className))
    def changeClass(self,oldClassName, newClassName):
        classNameList=[i.name for i in self.ontology]
        if(not oldClassName in classNameList):
            raise Exception('error in changeClass in Ontology: oldClassName "'+oldClassName+'" does not exist in this ontology')
        if(newClassName in [i.name for i in self.ontology]):
            raise Exeption('error in changrClass in Ontology: this newClass name "' + newClassName + '" already exists in this ontology')
        
        self.ontology[classNameList.index(oldClassName)].name=newClassName
        
        for class_ in self.ontology:
            for relationship_ in class_.relationships:
                if(relationship_.inClassName==oldClassName):
                    relationship_.inClassName=newClassName
            for entity_ in class_.entities:
                for entityRelationship_ in entity_.entityRelationships:
                    if(entityRelationship_.inClassName==oldNameClass):
                        entityRelationship_.inClassName=newNameClass
        
    def deleteClass(self,className,deep=False):
        if(not className in [i.name for i in self.ontology]):
            raise Exception('error in deleteClass in Ontology: this class name "' + className + '" already does not exist in this ontology')
        
        if deep==True:
            for class_ in self.ontology:
                if(class_.name==className):
                    continue
                for entity_ in class_.entities:
                    entity_.entityRelationships=[i for i in entity_.entityRelationships if not i.inClassName==className]
                class_.relationships=[i for i in class_.relationships if not i.inClassName==className]
            self.ontology.pop([i.name for i in self.ontology].index(className))
        else:
            for class_ in self.ontology:
                if(class_.name==className):
                    continue
                for entity_ in class_.entities:
                    for entityRelationship_ in entity_.entityRelationships:
                        if(entityRelationship_.inClassName==className):
                            raise Exception('error in deleteClass in Ontology: not deep deleting when class "'+className+'" has at leat one entity with an entity relationship')
                for relationship_ in class_.relationships:
                    if(relationship_.inClassName==className):
                        raise Exception('error in deleteClass in Ontology: not deep deleting when class "'+className+'" has at least one in relationship from other classes')
            self.ontology.pop([i.name for i in self.ontology].index(className))
    
    def addRelationship(self, relationshipName, outClassName, inClassName):
        classNameList=[i.name for i in self.ontology]
        
        if(not inClassName in classNameList):
            raise Exception('error in addRelationship in Ontology: inClassName "'+inClassName+'" does not exists in this ontology')
        if(not outClassName in classNameList):
            raise Exception('error in addRelationship in Ontology: outClassName "'+outClassName+'" does not exists in this ontology')
        
        outClass=self.ontology[classNameList.index(outClassName)]
        
        for relationship_ in outClass.relationships:
            if(relationship_.name==relationshipName):
                raise Exception('error in addRelationship in Ontology: name of relationship "'+relationshipName+'" is already exists in this ontology')
        
        outClass.relationships.append(Ontology.Class.Relationship(relationshipName,inClassName))
        
    def changeRelationship(self, oldRelationshipName, newRelationshipName, outClassName):
        classNameList=[i.name for i in self.ontology]
        
        if(not outClassName in classNameList):
            raise Exception('error in changeRelationship in Ontology: outClassName "'+outClassName+'" does not exists in this ontology')
        
        outClass=self.ontology[classNameList.index(outClassName)]
        relationshipNameList=[i.name for i in outClass.relationships]
        
        if(not oldRelationshipName in relationshipNameList):
            raise Exception('error in changeRelationship in Ontology: old relationship "'+oldRelationshipName+'" does not exist in this ontology for out class "'+outClassName+'"')
        if(newRelationshipName in relationshipNameList):
            raise Exception('error in changeRelationship in Ontology: new relationship "'+newRelationshipName+'" already exists in this ontology for out class "'+outClassName+'"')
        
        for entity_ in outClass.entities:
            for entityRelationship_ in entity_.entityRelationships:
                if(entityRelationship_.name==oldRelationshipName):
                    entityRelationship_.name=newRelationshipName
        
        outClass.relationships[relationshipNameList.index(oldRelationshipName)].name=newRelationshipName
        
    def deleteRelationship(self, relationshipName, outClassName, deep=False):
        classNameList=[i.name for i in self.ontology]
        
        if(not outClassName in classNameList):
            raise Exception('error in deleteRelationship in Ontology: outClassName "'+outClassName+'" does not exists in this ontology')
        
        outClass=self.ontology[classNameList.index(outClassName)]
        relationshipNameList=[i.name for i in outClass.relationships]
        
        if(not relationshipName in relationshipNameList):
            raise Exception('error in deleteRelationship in Ontology: relationship "'+relationshipName+'" does not exist in this ontology for out class "'+outClassName+'"')
        
        if deep==True:
            for entity_ in outClass.entities:
                entity_.entityRelationships=[i for i in entity_.entityRelationshops if not i.name==relationshipName]
            outClass.relationships.pop(relationshipNameList.index(relationshipName))
        else:
            for entity_ in outClass.entities:
                for entityRelationship_ in entity_.entityRelationships:
                    if(entityRelationship_.name==relationshipName):
                        raise Exception('error in deleteRelationship in Ontology: not deep deleting when relationship "'+relationshipName+'" for out class "'+outClassName+'" has at leat one appopriated entity relationship')
            outClass.relationships.pop(relationshipNameList.index(relationshipName))
    
    def addEntity(self, entityName, className):
        classNameList=[i.name for i in self.ontology]
        
        if(not className in classNameList):
            raise Exception('error in addEntity in Ontology: class "'+className+'" does not exists in this ontology')
        
        currentClass=self.ontology[classNameList.index(className)]
        entityNameList=[i.name for i in currentClass.entities]
        
        if(entityName in entityNameList):
            raise Exception('error in addEntity in Ontology: entity "'+entityName+'" already exists in this ontology')
        
        currentClass.entities.append(Ontology.Class.Entity(entityName))
        
    def changeEntity(self, oldEntityName, newEntityName, className):
        classNameList=[i.name for i in self.ontology]
        
        if(not className in classNameList):
            raise Exception('error in changeEntity in Ontology: class "'+className+'" does not exists in this ontology')
        
        currentClass=self.ontology[classNameList.index(className)]
        entityNameList=[i.name for i in currentClass.entities]
        
        if(newEntityName in entityNameList):
            raise Exception('error in changeEntity in Ontology: a new entity "'+newEntityName+'" already exists in this ontology')
        if(not oldEntityName in entityNameList):
            raise Exception('error in changeEntity in Ontology: an old entity "'+oldEntityName+'" does not exist in this ontology')
        
        for class_ in self.ontology:
            for entity_ in class_.entities:
                for entityRelationship_ in entity_.entityRelationships:
                    if(entityRelationship_.inClassName==className and entityRelationship_.inEntityName==oldEntityName):
                        entityRelationship_.inEntityName=inEntityName
        
        currentClass.entities[entityNameList.index(oldEntityName)].name=newEntityName
        
    def deleteEntity(self, entityName, className, deep=False):
        classNameList=[i.name for i in self.ontology]
        
        if(not className in classNameList):
            raise Exception('error in deleteEntity in Ontology: class "'+className+'" does not exists in this ontology')
        
        currentClass=self.ontology[classNameList.index(className)]
        entityNameList=[i.name for i in currentClass.entities]
        
        if(not entityName in entityNameList):
            raise Exception('error in deleteEntity in Ontology: an entity "'+entityName+'" does not exist in this ontology')
        
        if deep==True:
            for class_ in self.ontology:
                for entity_ in class_entities:
                    if(entity_.name==entityName and class_.name==className):
                        continue
                    for entityRelationship_ in entity_.entityRelationships:
                        if(entityRelationship_.inClassName==className and entityRelationship_.inEntityName==entityName):
                            raise Exception('error in deleteEntity in Ontology: not deep deleting when entity "'+entityName+'" for class "'+className+'" has at leat one appropriated entity relationship')
            currentClass.entities.pop(entityNameList.index(entityName))
        else:
            for class_ in self.ontology:
                for entity_ in class_.entities:
                    entity_.entityRelationships=[i for i in entity_.entityRelationships if not (i.inClassName==className and i.inEntityName==entityName)]
            currentClass.entities.pop(entityNameList.index(entityName))
    
    def addEntityRelationship(self, relationshipName, outClassName, outEntityName, inEntityName):
        classNameList=[i.name for i in self.ontology]
        
        if(not outClassName in classNameList):
            raise Exception('error in addEntityRelationship in Ontology: class "'+outClassName+'" does not exists in this ontology')
        
        outClass=self.ontology[classNameList.index(outClassName)]
        outRelationshipNameList=[i.name for i in outClass.relationships]
        outEntityNameList=[i.name for i in outClass.entities]
        
        if(not outEntityName in outEntityNameList):
            raise Exception('error in addEntityRelationship in Ontology: out entity "'+outEntityName+'" does not exist')
        if(not relationshipName in outRelationshipNameList):
            raise Exception('error in addEntityRelationship in Ontology: ralationship "'+relationshipName+'" for class "'+outClassName+'" does not exists')
        
        inClassName=outClass.relationships[outRelationshipNameList.index(relationshipName)].inClassName
        inClass=self.ontology[classNameList.index(inClassName)]
        
        inEntityNameList=[i.name for i in inClass.entities]
        
        if(not inEntityName in inEntityNameList):
            raise Exception('error in addEntityRelationship in Ontology: an in entity "'+inEntityName+'" for class "'+inClassName+'" does not exist')
        
        outEntity=outClass.entities[outEntityNameList.index(outEntityName)]
        
        if(not len([i for i in outEntity.entityRelationships if (i.name==relationshipName and i.inClassName==inClassName and i.inEntityName==inEntityName)])==0):
            raise Exception('error in addEntityRelationship in Ontology: an entity relationship "'+relationship+'" for an out class "'+outClassName+'" and an out entity "'+outEntityName+'" and an in entity "'+inEntityName+'" already esists')
        
        outEntity.entityRelationships.append(Ontology.Class.Entity.EntityRelationship(relationshipName, inClassName, inEntityName))
        
    def deleteEntityRelationship(self, relationshipName, outClassName, outEntityName, inEntityName):
        classNameList=[i.name for i in self.ontology]
        
        if(not outClassName in classNameList):
            raise Exception('error in deleteEntityRelationship in Ontology: class "'+outClassName+'" does not exists in this ontology')
        
        outClass=self.ontology[classNameList.index(outClassName)]
        outRelationshipNameList=[i.name for i in outClass.relationships]
        outEntityNameList=[i.name for i in outClass.entities]
        
        if(not outEntityName in outEntityNameList):
            raise Exception('error in deleteEntityRelationship in Ontology: out entity "'+outEntityName+'" does not exist')
        if(not relationshipName in outRelationshipNameList):
            raise Exception('error in deleteEntityRelationship in Ontology: ralationship "'+relationshipName+'" for class "'+outClassName+'" does not exists')
        
        inClassName=outClass.relationships[outRelationshipNameList.index(relationshipName)].inClassName
        inClass=self.ontology[classNameList.index(inClassName)]
        
        inEntityNameList=[i.name for i in inClass.entities]
        
        if(not inEntityName in inEntityNameList):
            raise Exception('error in deleteEntityRelationship in Ontology: an in entity "'+inEntityName+'" for class "'+inClassName+'" does not exist')
        
        outEntity=outClass.entities[outEntityNameList.index(outEntityName)]
        
        if(len([i for i in outEntity.entityRelationships if (i.name==relationshipName and i.inClassName==inClassName and i.inEntityName==inEntityName)])==0):
            raise Exception('error in deleteEntityRelationship in Ontology: an entity relationship "'+relationship+'" for an out class "'+outClassName+'" and an out entity "'+outEntityName+'" and an in entity "'+inEntityName+'" does not esists')
        
        #outEntity.entityRelationships.remove(Ontology.Class.Entity.EntityRelationship(relationshipName, inClassName, inEntityName))
        outEntity.entityRelationships.remove([i for i in outEntity.entityRelationships if (i.name==relationshipName and i.inClassName==inClassName and i.inEntityName==inEntityName)][0])
       
    def getAllClasses(self):
        return [i.name for i in self.ontology]
    def getAllRelationshipsForOutClass(self, className):
        classNameList=[i.name for i in self.ontology]
        
        if(not className in classNameList):
            raise Exception('error in getAllRelationshipsForOutClass in Ontology: a class "'+className+'" does not exists in this ontology')
        
        return [i.name for i in self.ontology[classNameList.index(className)].relationships]
    def getAllRelationshipsForOutClassToInClass(self, outClassName, inClassName):
        classNameList=[i.name for i in self.ontology]
        
        if(not inClassName in classNameList):
            raise Exception('error in getAllRelationshipsForOutClass in Ontology: an in class "'+inClassName+'" does not exists in this ontology')
        if(not outClassName in classNameList):
            raise Exception('error in getAllRelationshipsForOutClass in Ontology: an out class "'+outClassName+'" does not exists in this ontology')
        
        return [i.name for i in self.ontology[classNameList.index(outClassName)].relationships if i.inClassName==inClassName]
        
    def getAllEntitiesForClass(self, className):
        classNameList=[i.name for i in self.ontology]
        
        if(not className in classNameList):
            raise Exception('error in getAllEntitiesForClass in Ontology: a class "'+className+'" does not exists in this ontology')
        
        return [i.name for i in self.ontology[classNameList.index(className)].entities]
        
    def getAllRelationshipedEntitiesForOutEntity(self, outEntityName, outClassName):
        classNameList=[i.name for i in self.ontology]
        
        if(not outClassName in classNameList):
            raise Exception('error in getAllRelationshipedEntitiesForEntity in Ontology: an out class "'+outClassName+'" does not exists in this ontology')
        
        outEntityNamelist=[i.name for i in self.ontology[classNameList.index(outClassName)].entities]
        if(not outEntityName in outEntityNamelist):
            raise Exception('error in getAllRelationshipedEntitiesForEntity in Ontology: an out entity "'+outEntityName+'" for an out class "'+outClassName+'" does not exist')
        
        outEntity=self.ontology[classNameList.index(outClassName)].entities[outEntityNamelist.index(outEntityName)]
        
        return [(i.inClassName, i.inEntityName, i.name) for i in outEntity.entityRelationships]

    def getAllRelationshipedEntitiesForOutEntityForInClass(self, outEntityName, outClassName, inClassName):
        classNameList=[i.name for i in self.ontology]
        
        if(not outClassName in classNameList):
            raise Exception('error in getAllRelationshipedEntitiesForOutEntityForInClass in Ontology: an out class "'+outClassName+'" does not exists in this ontology')
        if(not inClassName in classNameList):
            raise Exception('error in getAllRelationshipedEntitiesForOutEntityForInClass in Ontology: an in class "'+inClassName+'" does not exists in this ontology')
        
        outEntityNamelist=[i.name for i in self.ontology[classNameList.index(outClassName)].entities]
        if(not outEntityName in outEntityNamelist):
            raise Exception('error in getAllRelationshipedEntitiesForOutEntityForInClass in Ontology: an out entity "'+outEntityName+'" for an out class "'+outClassName+'" does not exist')
        
        outEntity=self.ontology[classNameList.index(outClassName)].entities[outEntityNamelist.index(outEntityName)]
        
        return [(i.inEntityName, i.name) for i in outEntity.entityRelationships if i.inClassName==inClassName]
    
    def getAllRelationshipedEntitiesForOutEntityForRelationship(self, outEntityName, outClassName, relationshipName):
        classNameList=[i.name for i in self.ontology]
        
        if(not outClassName in classNameList):
            raise Exception('error in getAllRelationshipedEntitiesForOutEntityForRelationship in Ontology: an out class "'+outClassName+'" does not exists in this ontology')
        
        relationshipNameList=[i.name for i in self.ontology[classNameList.index(outClassName)].relationships]
        
        if(not relationshipName in relationshipNameList):
            raise Exception('error in getAllRelationshipedEntitiesForOutEntityForRelationship in Ontology: an relationship "'+relationshipName+'" for class "'+outClassName+'" does not exists in this ontology')
        
        outEntityNamelist=[i.name for i in self.ontology[classNameList.index(outClassName)].entities]
        if(not outEntityName in outEntityNamelist):
            raise Exceptino('error in getAllRelationshipedEntitiesForOutEntityForRelationship in Ontology: an out entity "'+outEntityName+'" for an out class "'+outClassName+'" does not exist')
        
        outEntity=self.ontology[classNameList.index(outClassName)].entities[outEntityNamelist.index(outEntityName)]
        
        return [i.inEntityName for i in outEntity.entityRelationships if i.name==relationshipName]
    
    directoryForSavedOntology='saved'
    def saveToFile(self, fileName):
        file=open(self.directoryForSavedOntology+'/'+fileName,'bw')
        pickle.dump(self, file)
        file.close()
    def loadFromFile(self, fileName):
        file=open(self.directoryForSavedOntology+'/'+fileName,'br')
        self=pickle.load(file)
        file.close()
    def crear(self):
        seld.ontology=[]
