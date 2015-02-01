# convert choices to tuples

#with open('choices.py') as f:
#    content = f.readlines();
#
#with open('new_choices.py', 'w') as f:
#    for line in content:
#        f.write('(\'' + line.strip() + '\', \'' + line.strip() + '\'),\n')


# convert choices to options

with open('select.py') as f:
    content = f.readlines()

with open('test.py', 'w') as f:
    for line in content:
        f.write('<option value="'+line.strip()+'">'+line.strip()+'</option>\n')
  
    
    
