import { NgModule } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";
import { FormsModule } from "@angular/forms";
import { HttpModule } from "@angular/http";

import { AppComponent } from "./app.component";
import { MaterialModule } from "../material.module";
import { RoutingModule } from "./app.routing";

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
        AppComponent,
        MapComponent,
        ContactComponent,
    ],
    providers: [
        MapService,
        ContactService,
    ],
    bootstrap: [ AppComponent ],
})
export class AppModule {}
