import { Component, OnInit } from "@angular/core";
import { ActivatedRoute, Params } from "@angular/router";
import { Observable } from "rxjs/Observable";

import { Event, EventService } from "./../";

@Component({
    moduleId: module.id,
    selector: "cg-event-detail-page",
    templateUrl: "eventDetail.component.html",
})
export class EventDetailComponent implements OnInit {
    public tweetIds: Observable<string[]> = this.eventService.getTweetIds(this.event);
    private event: Event;
    private errorMessage: string;

    constructor(private eventService: EventService, private route: ActivatedRoute) {}

    public ngOnInit() {
        this.route.params.forEach((params: Params) => {
            let id = + params["id"];
            this.getEvent(id);
        });
    }

    public clearError() {
        this.errorMessage = "";
    }

    private getEvent(id: number) {
        this.eventService.getEvent(id).subscribe(
            event => this.event = event,
            error => this.setErrorMessage(<any> error),
        );
    }

    private setErrorMessage(errorMessage: string) {
        this.errorMessage = errorMessage;
    }
}
