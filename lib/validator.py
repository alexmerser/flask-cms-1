class Validator():
    def __init__(self):
        self.errors = []
        self.builtin_rules = {'required' : [self.required, 'Please enter a {0}'],
            'maxlength' : [self.maxlength,'Use {0} or less chars'],
            'minlength' : [self.minlength,'Use {0} or more chars'],
            'numeric'  : [self.numeric,'Please enter a number'],
            'min'  : [self.min,'Use {0} or a number bigger'],
            'max'  : [self.max,'Use {0} or a number smaller']
            }
    
    def required(self,val,param):
        return len(val) > 0
    
    def maxlength(self, val, param):
        return len(val) <= param

    def minlength(self, val, param):
        return len(val) >= param
    
    def max(self, val, param):
        try:
            return float(val) <= param
        except ValueError:
            return False

    def min(self, val, param):
        try:
            return float(val) >= param
        except ValueError:
            return False
    
    def numeric(self, val, param):
        try:
            float(val)
            return True
        except ValueError:
            return False
         
    
    def validate(self, values):
        """
        Arguments:
            values -- The input values map to be validate
        """
        errors = []
        fields = values.keys()
        
        for field in self.rules:
            if field in fields:
                for rule_name in self.rules[field]:
                    validate_func = None
                    msg = None
                    rule = self.rules[field][rule_name]
                    val = values.get(field)
                    criterion = rule[1]
                    if rule_name in self.builtin_rules.keys():
                        validate_func = self.builtin_rules[rule_name][0]
                        msg = self.builtin_rules[rule_name][1]
                        if rule_name == 'required':
                            msg = msg.format(field)
                        elif rule_name == 'maxlength' or rule_name == 'minlength':
                            msg = msg.format(criterion)
                    else:
                        validate_func = rule[0]
                        
                        msg = rule[2]
                        
                    if not validate_func(val, rule[1]):
                        errors.append({'field':field, 'rule':rule_name, 'message': msg})
        
        return errors   
    
