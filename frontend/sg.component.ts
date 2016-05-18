import { Component, OnInit } from "@angular/core";
import { Routes, Router, ROUTER_DIRECTIVES } from "@angular/router";

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
export class StrassengezwitscherComponent implements OnInit {
    constructor(private router: Router) {}

    ngOnInit() {
        this.router.navigate(["/"]);
    }
}
