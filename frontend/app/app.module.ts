import { NgModule } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";
import { FormsModule } from "@angular/forms";
import { HttpModule } from "@angular/http";

import { MdButtonModule } from "@angular2-material/button";
import { MdCheckboxModule } from "@angular2-material/checkbox";
import { MdCardModule } from "@angular2-material/card";
import { MdIconModule } from "@angular2-material/icon";
import { MdInputModule } from "@angular2-material/input";
import { MdMenuModule } from "@angular2-material/menu";
import { MdRadioModule } from "@angular2-material/radio";
import { MdSlideToggleModule } from "@angular2-material/slide-toggle";
import { MdToolbarModule } from "@angular2-material/toolbar";
import { MdTooltipModule } from "@angular2-material/tooltip";

import { AppComponent } from "./app.component";
import { RoutingModule } from "./app.routing";

import { MapComponent, MapService } from "./map";
import { ContactComponent, ContactService } from "./contact";
import { FacebookPageComponent } from "./facebook";
import { EventComponent } from "./events";
import { ImprintComponent } from "./imprint";
import { AboutComponent } from "./about";

@NgModule({
    imports: [
        BrowserModule,
        FormsModule,
        HttpModule,
        RoutingModule,
        MdButtonModule.forRoot(),
        MdCardModule.forRoot(),
        MdCheckboxModule.forRoot(),
        MdMenuModule.forRoot(),
        MdIconModule.forRoot(),
        MdInputModule.forRoot(),
        MdRadioModule.forRoot(),
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
        ImprintComponent,
        AboutComponent,
    ],
    providers: [
        MapService,
        ContactService,
    ],
    bootstrap: [ AppComponent ],
})
export class AppModule {}
