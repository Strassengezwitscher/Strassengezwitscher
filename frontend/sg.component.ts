import { Component, OnInit } from "@angular/core";
import { NavBarComponent } from "./navbar.component";
import { MapComponent } from "./map.component";

@Component({
    selector: "sg-app",
    templateUrl: "sg.component.html",
    directives: [NavBarComponent, MapComponent]
})
export class StrassengezwitscherComponent {}
