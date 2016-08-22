import { Component, ViewEncapsulation } from "@angular/core";
import { ROUTER_DIRECTIVES } from "@angular/router";

// Add the RxJS Observable operators we need in this app.
import "./rxjs-operators";

@Component({
    moduleId: module.id,
    selector: "cg-app",
    templateUrl: "cg.component.html",
    styleUrls: ["cg.component.css"],
    encapsulation: ViewEncapsulation.None,
    directives: [
        ROUTER_DIRECTIVES,
    ],
})
export class CrowdgezwitscherComponent {}
