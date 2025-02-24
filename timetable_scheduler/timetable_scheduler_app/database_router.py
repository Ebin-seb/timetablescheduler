class CollegeDatabaseRouter:
    def db_for_read(self,model,**hints):
        request = hints.get('request')
        if request and hasattr(request.user,'college'):
            return f'college_{request.user.college.id}'
        return 'default'
    
    def db_for_write(self,model,**hints):
        request = hints.get('request')
        if request and hasattr(request.user,'college'):
            return f'college_{request.user.college.id}'
        return 'default'
    
    def allow_relation(self,obj1,obj2,**hints):
        if obj1._state.db == obj2._state.db:
            return True
        return None
    
    def allow_migrate(self,db,app_label,model_name=None,**hints):
        if db == 'default':
            return app_label == 'global_admin'
        return True
    
