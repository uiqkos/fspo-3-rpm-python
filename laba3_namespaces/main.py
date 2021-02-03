
class Namespace:
    def __init__(self, name, parent=None, children=[]):
        self.name = name
        self.variables = []
        self.parent = parent
        self.children = children


def get(namespace: Namespace, variable):
    if variable in namespace.variables:
        return namespace.name
    if namespace.parent is not None:
        return get(namespace.parent, variable)
    return 'None'


if __name__ == '__main__':
    namespaces = {
        'global': {
            'name': 'global',
            'variables': []
        }
    }
    for i in range(int(input())):
        command, namespace_name, arg = input().split()

        if command == 'create':
            parent = namespaces[arg]
            new_namespace = Namespace(namespace_name, parent)

            namespaces[namespace_name] = new_namespace
            parent.children.append(new_namespace)

        elif command == 'get':
            print(get(namespaces[namespace_name], arg))

        elif command == 'add':
            namespaces[namespace_name].variables.append(arg)


