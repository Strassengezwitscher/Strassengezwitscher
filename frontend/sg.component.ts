import { Component, OnInit } from "@angular/core";
import { Routes, Router, ROUTER_DIRECTIVES } from "@angular/router";

// Add the RxJS Observable operators we need in this app.
import './rxjs-operators';

import { NavBarComponent } from "./navbar.component";
import { MapComponent } from "./map.component";
import { ContactComponent } from "./contact.component";

@Component({
    selector: "sg-app",
    templateUrl: "sg.component.html",
    directives: [
        ROUTER_DIRECTIVES,
        NavBarComponent
    ]
})
@Routes([
    { path: "/", component: MapComponent },
    { path: "/contact", component: ContactComponent }
])
export class StrassengezwitscherComponent {}
