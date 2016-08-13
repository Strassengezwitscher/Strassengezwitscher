import { NgModule } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";
import { FormsModule } from "@angular/forms";
import { HttpModule } from "@angular/http";

import { CrowdgezwitscherComponent } from "./cg.component";
import { routing } from "./cg.routing";

import { MapComponent } from "./map.component";
import { ContactComponent } from "./contact.component";

import { MapService } from "./map.service";
import { ContactService } from "./contact.service";

@NgModule({
    imports: [
        BrowserModule,
        FormsModule,
        HttpModule,
        routing,
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
