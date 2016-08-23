import { NgModule } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";
import { FormsModule } from "@angular/forms";
import { HttpModule } from "@angular/http";

import { CrowdgezwitscherComponent } from "./cg.component";
import { MaterialModule } from "./material.module";
import { RoutingModule } from "./cg.routing";

import { MapComponent } from "./map.component";
import { ContactComponent } from "./contact.component";
import { ContactSuccessComponent } from "./contactSuccess.component";

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
        CrowdgezwitscherComponent,
        MapComponent,
        ContactComponent,
        ContactSuccessComponent,
    ],
    providers: [
        MapService,
        ContactService,
    ],
    bootstrap: [ CrowdgezwitscherComponent ],
})
export class CrowdgezwitscherModule {}
