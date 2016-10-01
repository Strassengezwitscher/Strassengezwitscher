export function RollupModuleProvider(params: any) {
    return function (target: any) {
        // Setup the 'module' variable globally. The rollup javascript has its own module system, but there is still a
        // reference to the Commonjs module.id in the code, so setup a module object to allow that code to execute
        // without throwing an exception
        try {
            // In dev mode with commonjs the following line will execute without a problem
            // In AoT mode with rollup the following line will trigger an exception that will be
            // caught and handled to allow the AoT build to run without issue
            const testIfRunningWithCommonJSandModuleIsAvailable = module.id;
        } catch (e) {
            // Declare Module for rollup based production builds.
            // When running dev builds CommonJS automatically provides the module definition
            let globalScope: any;
            if (typeof window === "undefined") {
                globalScope = global;
            } else {
                globalScope = window;
            }
            globalScope.module = "test";
            try {
                const moduleShouldBeAvailable = module;
            } catch (e) {
                // Our attempt to register module failed so we are not in an unrecoverable error state.
                console.error("Module not defined");
            }
        }
    };
}
