class FutureFilterRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        print("model._meta.app_label = " + model._meta.app_label)
        if model._meta.app_label == 'future':
            return 'future_filter'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'future':
            return 'future_filter'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'future' or \
           obj2._meta.app_label == 'future':
           return True
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        #if app_label == 'future':
        #    return db == 'future_filter'
        return None