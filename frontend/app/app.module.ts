import { NgModule } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";
import { FormsModule } from "@angular/forms";
import { HttpModule, JsonpModule } from "@angular/http";

import { MdButtonModule } from "@angular2-material/button";
import { MdCheckboxModule } from "@angular2-material/checkbox";
import { MdSlideToggleModule } from "@angular2-material/slide-toggle";
import { MdCardModule } from "@angular2-material/card";
import { MdIconModule } from "@angular2-material/icon";
import { MdInputModule } from "@angular2-material/input";
import { MdMenuModule } from "@angular2-material/menu";
import { MdToolbarModule } from "@angular2-material/toolbar";
import { MdTooltipModule } from "@angular2-material/tooltip";

import { AppComponent } from "./app.component";
import { RoutingModule } from "./app.routing";

import { MapComponent, MapService } from "./map";
import { ContactComponent, ContactService } from "./contact";
import { FacebookPageComponent } from "./facebook";
import { EventComponent, EventDetailComponent, EventService } from "./events";
import { ImprintComponent } from "./imprint";
import { AboutComponent } from "./about";
import { TweetComponent, TwitterService } from "./twitter";

@NgModule({
    imports: [
        BrowserModule,
        FormsModule,
        HttpModule,
        JsonpModule,
        RoutingModule,
        MdButtonModule.forRoot(),
        MdCardModule.forRoot(),
        MdCheckboxModule.forRoot(),
        MdMenuModule.forRoot(),
        MdIconModule.forRoot(),
        MdInputModule.forRoot(),
        MdSlideToggleModule.forRoot(),
        MdToolbarModule.forRoot(),
        MdTooltipModule.forRoot(),
    ],
    declarations: [
        AboutComponent,
        AppComponent,
        ContactComponent,
        EventComponent,
        EventDetailComponent,
        FacebookPageComponent,
        ImprintComponent,
        MapComponent,
        TweetComponent,
    ],
    providers: [
        ContactService,
        EventService,
        MapService,
        TwitterService,
    ],
    bootstrap: [ AppComponent ],
})
export class AppModule {}
