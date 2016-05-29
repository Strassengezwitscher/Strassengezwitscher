import { Component, OnInit } from "@angular/core";
import { ROUTER_DIRECTIVES } from "@angular/router";

@Component({
    selector: "nav-bar",
    templateUrl: "navbar.component.html",
    directives: [ROUTER_DIRECTIVES]
})
export class NavBarComponent {}
