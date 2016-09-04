import { NgModule } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";
import { FormsModule } from "@angular/forms";
import { HttpModule } from "@angular/http";

import { CrowdgezwitscherComponent } from "./cg.component";
import { MaterialModule } from "../material.module";
import { RoutingModule } from "./cg.routing";

import { MapComponent } from "../map/map.component";
import { ContactComponent } from "../contact/contact.component";

import { MapService } from "../map/map.service";
import { ContactService } from "../contact/contact.service";

@NgModule({
    imports: [
        BrowserModule,
        FormsModule,
        HttpModule,
        MaterialModule,
        RoutingModule,
    ],
    declarations: [
        CrowdgezwitscherComponent,
        MapComponent,
        ContactComponent,
    ],
    providers: [
        MapService,
        ContactService,
    ],
    bootstrap: [ CrowdgezwitscherComponent ],
})
export class CrowdgezwitscherModule {}
