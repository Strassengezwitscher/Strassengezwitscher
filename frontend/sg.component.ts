import { Component } from "@angular/core";
import { ROUTER_DIRECTIVES } from "@angular/router";
import { MdAnchor } from "@angular2-material/button/button";
import { MdIcon, MdIconRegistry } from "@angular2-material/icon/icon";
import { MdToolbar } from "@angular2-material/toolbar/toolbar";

// Add the RxJS Observable operators we need in this app.
import "./rxjs-operators";

@Component({
    selector: "sg-app",
    templateUrl: "sg.component.html",
    viewProviders: [MdIconRegistry],
    directives: [
        ROUTER_DIRECTIVES,
        MdAnchor,
        MdIcon,
        MdToolbar,
    ],
})
export class StrassengezwitscherComponent {}
