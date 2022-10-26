import os
import re


env = dict(os.environ)
template_dir = os.path.join(os.getcwd(), 'templates')


if __name__ == '__main__':
    # Get a list of all templates in current dir
    template_file_name_list = [file_name for file_name in os.listdir(
        template_dir) if '.yaml' in file_name]

    # Read all templates
    for file_name in template_file_name_list:
        file_path = os.path.join(template_dir, file_name)

        missed_placeholder_list: list[str] = []
        new_content_string_list: list[str] = []

        with open(file_path, mode='r') as f:
            content_string_list = f.readlines()

        # Replace placeholders marked as ${{}} with host env vars
        for line in content_string_list:
            for env_name in env.keys():
                line = line.replace(f'${{{{{env_name}}}}}', env[env_name])
            # Verify that every placeholder was replaced
            for missed_placeholder_on_this_line in re.findall(r'\$\{\{.*?\}\}', line):
                missed_placeholder_list.append(missed_placeholder_on_this_line)

            new_content_string_list.append(line)

        if len(missed_placeholder_list) != 0:
            print(
                "You don't have some env vars set up that are used in template, see list below:")
            for missed_placeholder in missed_placeholder_list:
                missed_placeholder = missed_placeholder.replace(r'${{', '')\
                                                       .replace(r'}}', '')
                print(missed_placeholder)
            raise KeyError("Env vars not defined")

        new_file_name = file_name.replace('.tpl', '')
        with open(file=new_file_name, mode='w') as f:
            f.writelines(new_content_string_list)
