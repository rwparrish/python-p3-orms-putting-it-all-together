import sqlite3
import ipdb

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    
    def __init__(self, name, breed, id=None):
        self.name = name
        self.breed = breed
        self.id = id
      
        
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """

        CURSOR.execute(sql)
        
        
    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs 
        """

        CURSOR.execute(sql)
        
        
    def save(self):
        sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.breed))
        CONN.commit()
        
        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]
        
        
    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog
    
    
    @classmethod
    def new_from_db(cls, dogArr):
        
        newDog = cls(dogArr[1], dogArr[2], dogArr[0])
        # newDog.id = dogArr[0] - moved to __init__
        return newDog
    
    
    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM dogs
        """

        all = CURSOR.execute(sql).fetchall()
        allDogs = []
        for dog in all:
            newDog = cls.new_from_db(dog)
            allDogs.append(newDog)
            
        return allDogs
    
       
    @classmethod
    def find_by_name(cls, name):
        
        sql = '''
            SELECT * FROM dogs 
            WHERE name = ?
            LIMIT 1
        '''
       
        row = CURSOR.execute(sql, (name,)).fetchone()
        
        if row:
            return cls.new_from_db(row)
        else:
            print('Dog not found')
    
    
    
    @classmethod
    def find_by_id(cls, id):
        
        sql = '''
            SELECT * FROM dogs 
            WHERE id = ?
            LIMIT 1
        '''
       
        row = CURSOR.execute(sql, (id,)).fetchone()
        
        if row:
            return cls.new_from_db(row)
        else:
            print('Dog not found')
       
        
       
