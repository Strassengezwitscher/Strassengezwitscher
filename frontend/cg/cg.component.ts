import { Component } from "@angular/core";
import { ROUTER_DIRECTIVES } from "@angular/router";

// Add the RxJS Observable operators we need in this app.
import "../rxjs-operators";

@Component({
    moduleId: module.id,
    selector: "cg-app",
    templateUrl: "cg.component.html",
    directives: [
        ROUTER_DIRECTIVES,
    ],
})
export class CrowdgezwitscherComponent {}
