import copy


class PrettyPrinter(object):
    def __str__(self):

        lines = [self.__class__.__name__ + ':']
        for key, val in vars(self).items():
            if type(val) == list:
                for v in val:
                    try:
                        copy.deepcopy(v)
                        s = " (T) "
                    except:
                        s = " (F) "
                    lines += '{}{}'.format(s, v).split('\n')

            elif type(val) == dict:
                for k in val:
                    v = val[k]
                    try:
                        copy.deepcopy(v)
                        s = " (T) "
                    except:
                        s = " (F) "
                    lines += '{}{}: {}'.format(s, k, v).split('\n')
            
            else:

                try:
                    copy.deepcopy(val)
                    s = " (T) "
                except:
                    s = " (F) "

                lines += '{}{}: {}'.format(s, key, val).split('\n')
        return '\n    '.join(lines)