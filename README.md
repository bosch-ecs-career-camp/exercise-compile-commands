# Function to convert log into json file with following content

- @compileCommands function which needs to generate the final json looking like this:
```json
    [
        { "directory": "/home/user/llvm/build",
            "arguments": ["/usr/bin/clang++", "-Irelative", "-DSOMEDEF=With spaces, quotes and \\-es.", "-c", "-o", "file.o", "file.cc"],
            "file": "file.cc" 
        },

        { "directory": "/home/user/llvm/build",
            "command": "/usr/bin/clang++ -Irelative -DSOMEDEF=\"With spaces, quotes and \\-es.\" -c -o file.o file.cc",
            "file": "file2.cc" 
        },
        ...
    ]
```