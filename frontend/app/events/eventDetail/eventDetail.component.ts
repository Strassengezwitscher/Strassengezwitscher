import { Component, OnInit } from "@angular/core";
import { ActivatedRoute, Params } from "@angular/router";

import { Event } from "../shared/event.model";
import { EventService } from "../shared/event.service";

declare var twttr: any;

@Component({
    moduleId: module.id,
    selector: "cg-event-detail-page",
    templateUrl: "eventDetail.component.html",
    styleUrls: ["eventDetail.component.css"],
})
export class EventDetailComponent implements OnInit {
    public event: Event;
    public tweetIds: string[] = null;
    public errorMessage: string;
    public twttrIsBlocked: boolean = (typeof twttr === "undefined");

    constructor(private eventService: EventService, private route: ActivatedRoute) {}

    public ngOnInit() {
        this.route.params.forEach((params: Params) => {
            let id = + params["id"];
            this.getEvent(id);
        });
    }

    public onRefresh() {
        this.eventService.getTweetIds(this.event).subscribe(
            tweetIds => this.tweetIds = tweetIds
        );
    }

    private getEvent(id: number) {
        this.eventService.getEvent(id).subscribe(
            event => this.setEvent(event),
            error => this.setErrorMessage(<any> error),
        );
    }

    private setErrorMessage(errorMessage: string) {
        this.errorMessage = errorMessage;
    }

    private setEvent(event: Event) {
        this.event = event;
        if (this.event && this.event.coverage) {
            this.eventService.getTweetIds(this.event).subscribe(
                tweetIds => this.tweetIds = tweetIds
            );
        }
    }
}
