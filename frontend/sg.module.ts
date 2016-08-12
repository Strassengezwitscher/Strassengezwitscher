import { NgModule } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";
import { FormsModule } from "@angular/forms";
import { HttpModule } from "@angular/http";

import { StrassengezwitscherComponent } from "./sg.component";
import { MaterialModule } from "./material.module";
import { RoutingModule } from "./sg.routing";

import { MapComponent } from "./map.component";
import { ContactComponent } from "./contact.component";

import { MapService } from "./map.service";
import { ContactService } from "./contact.service";

@NgModule({
    imports: [
        BrowserModule,
        FormsModule,
        HttpModule,
        MaterialModule,
        RoutingModule,
    ],
    declarations: [
        StrassengezwitscherComponent,
        MapComponent,
        ContactComponent,
    ],
    providers: [
        MapService,
        ContactService,
    ],
    bootstrap: [ StrassengezwitscherComponent ],
})
export class StrassengezwitscherModule {}
