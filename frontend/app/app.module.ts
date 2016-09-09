import { NgModule } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";
import { FormsModule } from "@angular/forms";
import { HttpModule } from "@angular/http";

import { MdButtonModule } from "@angular2-material/button";
import { MdCheckboxModule } from "@angular2-material/checkbox";
import { MdSlideToggleModule } from "@angular2-material/slide-toggle";
import { MdCardModule } from "@angular2-material/card";
import { MdIconModule } from "@angular2-material/icon";
import { MdInputModule } from "@angular2-material/input";
import { MdToolbarModule } from "@angular2-material/toolbar";
import { MdTooltipModule } from "@angular2-material/tooltip";

import { AppComponent } from "./app.component";
import { RoutingModule } from "./app.routing";

import { MapComponent, MapService } from "./map";
import { ContactComponent, ContactService } from "./contact";
import { FacebookPageComponent } from "./facebook";
import { EventComponent } from "./events";

@NgModule({
    imports: [
        BrowserModule,
        FormsModule,
        HttpModule,
        RoutingModule,
        MdButtonModule.forRoot(),
        MdCardModule.forRoot(),
        MdCheckboxModule.forRoot(),
        MdIconModule.forRoot(),
        MdInputModule.forRoot(),
        MdSlideToggleModule.forRoot(),
        MdToolbarModule.forRoot(),
        MdTooltipModule.forRoot(),
    ],
    declarations: [
        AppComponent,
        MapComponent,
        ContactComponent,
        FacebookPageComponent,
        EventComponent,
    ],
    providers: [
        MapService,
        ContactService,
    ],
    bootstrap: [ AppComponent ],
})
export class AppModule {}
