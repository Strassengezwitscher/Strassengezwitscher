import { NgModule } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";
import { FormsModule } from "@angular/forms";
import { HttpModule } from "@angular/http";

import { AppComponent } from "./app.component";
import { MaterialModule } from "./shared/material.module";
import { RoutingModule } from "./app.routing";

import { MapComponent, MapService } from "./map/index";
import { ContactComponent, ContactService } from "./contact/index";

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
