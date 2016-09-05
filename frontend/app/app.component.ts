import { Component } from "@angular/core";
import { ROUTER_DIRECTIVES } from "@angular/router";

// Add the RxJS Observable operators we need in this app.
import "./shared/rxjs-operators";

@Component({
    moduleId: module.id,
    selector: "cg-app",
    templateUrl: "app.component.html",
    directives: [
        ROUTER_DIRECTIVES,
    ],
})
export class AppComponent {}
