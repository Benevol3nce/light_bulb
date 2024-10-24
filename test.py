try:
    with open('C:/ncs/projects/light_bulb/zephyr/scripts/schemas/build-schema.yml') as f:
        content = f.read()
        print('File opened successfully')
        print('File content:')
        print(content)
except Exception as e:
    print(f'Error opening file: {e}')