
# $Id$ $Date$


import re

class preload:
    def select_command(self, elements, table):
        first = True
        select='SELECT '
        for name in elements:
            if first:
                first = False
                select += "`{}`".format(name)
            elif not first:
                select += ", `{}`".format(name)
        select += " FROM `{}` LIMIT 3".format(table)
        #print(select)
        return select

    def declarations(self, names, name_type, StructreName, table_name, assigned_command, select_command):


        #print(names, name_type, structre_name, table_name)
        #print(variable_template.replace('{}',structre_name))
        read_data_from_select = '''
        // Place into XXXService.cpp:

        {
            ostringstream os;
            select_command
            int n = dbc->Query(os.str());
            if( n <= 0 ) {
                Log(QMANS, QMANS_ERROR, "ERROR: Preload() Not live calls in 'queue_data'\n");
                return false;
            }
        }

        std::unique_ptr<M{}_t> p{}(new M{}_t);
        int col;
        while( dbc->NextRow() ) {
            col=0;
            assign_command
            // pbxIdOfId(account_id, parentId);               // update PbxId table
            p{}->emplace( M{}_t::value_type( account_id, {    // account_id is the key
            // names go here, seperated by ','
            NAMES
            } ));
        }

        Log(QMANS, QMANS_DEBUG, "Loaded table_name: %zu, last column: %u\\n", p{}->size(), col);
        Log(QMANS, QMANS_DEBUG, "   (Updated PMPbxIds_m: %zu)\\n", PMPbxIds_m->size());

        M{}Lock_m.write_lock();
        PM{}_m.swap(p{});
        M{}Lock_m.unlock();

        '''.replace('table_name', table_name).replace('{}',StructreName).replace('assign_command',assigned_command).replace('select_command',select_command).replace('NAMES', ',\n\t'.join(names))
        #print(read_data_from_select)
        return read_data_from_select

    def define_structure(self, names, name_type, StructreName, table_name):
        fields ='\n'
        first = True
        for name in name_type.keys():
            fields += "\t{} {};\n".format(name_type[name], name)

        variable_template ='''
    // Place into XXXService.hpp:

    struct {}_t {
        FIELDS
    };
    typedef std::map<ID_t, {}_t>    M{}_t;

    mutable RW_Mutex                M{}Lock_m;
    std::unique_ptr<M{}_t>          PM{}_m;
    '''.replace('{}', StructreName).replace('FIELDS', fields)
        #print(variable_template)
        return variable_template

    def assign_command(self, names, name_type):
        command='\n'
        first = True
        for name in name_type.keys():
            #print(name)
            #print(name_type[name])
            if first:
                index = ''
                first = False
            else:
                index = '++col'
            if 'int32_t' in name_type[name]:
                command += "\t{} {} = atol(STR(dbc->RValue({})));\n".format(name_type[name], name, index)
            elif 'int64_t' in name_type[name]:
                command += "\t{} {} = atoll(STR(dbc->RValue({})));\n".format(name_type[name], name, index)
            elif 'uint32_t' in name_type[name]:
                command += "\t{} {} = atol(STR(dbc->RValue({})));\n".format(name_type[name], name, index)
            elif 'uint64_t' in name_type[name]:
                command += "\t{} {} = atoll(STR(dbc->RValue({})));\n".format(name_type[name], name, index)
            elif 'double_t' in name_type[name]:
                command += "\t{} {} = atof(STR(dbc->RValue({})));\n".format(name_type[name], name, index)
            else:
                command += "\t{} {} = STR(dbc->RValue({}));\n".format(name_type[name], name, index)

        return command


class make_xlat():
    def __init__(self, *args, **kwds):
        self.adict = dict(*args, **kwds)
        self.rx = self.make_rx( )
    def make_rx(self):
        return re.compile('|'.join(map(re.escape, self.adict)))
    def one_xlat(self, match):
        return self.adict[match.group(0)]
    def __call__(self, text):
        return self.rx.sub(self.one_xlat, text)

class make_xlat_by_whole_words(make_xlat):
    def make_rx(self):
        return re.compile(r'\b%s\b' % r'\b|\b'.join(map(re.escape, self.adict)))

class make_xlat_re(make_xlat):
    def make_rx(self):
        return re.compile('|'.join(self.adict))
    def dedictkey(self, text):
        for key in self.adict.keys():
            if re.search(key, text):
                return key
    def one_xlat(self, match):
        return self.adict[self.dedictkey(match.group(0))]


if __name__ == '__main__':
    text = "Larry Wall is the creator of Perl 123"
    adict = {
     "Larry Wall" : "Guido van Rossum",
     "creator" : "Benevolent Dictator for Life",
     "Perl" : "Python"
    }
    redict = {
     "Larry Wall" : "Guido van Rossum",
     "creator" : "Benevolent Dictator for Life",
     "(?:Perl|Ruby)" : "Python",
     "(\d+)" : "digits"
    }
    translate = make_xlat(adict)
    transwords = make_xlat_by_whole_words(adict)
    transre = make_xlat_re(redict)
    print (translate(text))
    print (transwords(text))
    print (transre(text))
