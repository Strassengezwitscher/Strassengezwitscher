import { Component, ViewEncapsulation } from "@angular/core";
import { RollupModuleProvider } from "./rollup-module.provider";


@RollupModuleProvider({})
@Component({
    selector: "cg-app",
    templateUrl: "app.component.html",
    styleUrls: ["app.component.css"],
    encapsulation: ViewEncapsulation.None,
})
export class AppComponent {}
