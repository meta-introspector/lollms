import docker
import json

def inspect():
    client = docker.from_env()
    data = {}
    keys = [] #any secrets we found
    for container in client.containers.list():
        attrs = {}
        for x in container.attrs:
            #print("attr",x)
            if x == "Config":
                attrs[x] = container.attrs[x]
                config = container.attrs[x]
                envs = config["Env"]
                #print(envs)
                clean = []
                for y in envs:
                    #print(y)
                    for z in ["KEY", "GITHUB_PAT", "SECRET","TOKEN" , "PASS"]:
                        if z in y.upper():                        
                            parts = y.split("=")
                            keys.append(parts[1])
                            parts[1]="redacted"
                            y = "=".join(parts)
                    clean.append(y)
                config["Env"] = clean
                attrs[x]["Env"] = clean
            else:
                attrs[x] = container.attrs[x]

            #print(x)

        #attrs2 = container.attrs
        #attrs2['envs'] = envs
        #print( attrs['Config']['Env'])
        #print( keys)
        toclean = json.dumps(dict(
            attrs = attrs,
            logs = str(container.logs())
            ))
        for k in keys:
            toclean = toclean.replace(k,"redacted2")
            
        data[container.name] = toclean #only clean data
        return data
if __name__ == "__main__":
    print(inspect())
