import { NgModule } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";
import { FormsModule } from "@angular/forms";
import { HttpModule } from "@angular/http";

import { MaterialModule } from "@angular/material";

import { AppComponent } from "./app.component";
import { RoutingModule } from "./app.routing";

import { MapComponent, MapService } from "./map";
import { ContactComponent, ContactService } from "./contact";
import { FacebookPageComponent } from "./facebook";
import { EventComponent, EventDetailComponent, EventService } from "./events";
import { ImprintComponent } from "./imprint";
import { AboutComponent } from "./about";
import { BlogComponent } from "./blog";

@NgModule({
    imports: [
        BrowserModule,
        FormsModule,
        HttpModule,
        RoutingModule,
        MaterialModule.forRoot(),
    ],
    declarations: [
        AppComponent,
        BlogComponent,
        MapComponent,
        ContactComponent,
        FacebookPageComponent,
        EventComponent,
        EventDetailComponent,
        ImprintComponent,
        AboutComponent,
    ],
    providers: [
        MapService,
        ContactService,
        EventService,
    ],
    bootstrap: [ AppComponent ],
})
export class AppModule {}
