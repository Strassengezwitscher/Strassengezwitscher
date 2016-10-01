import { Component, OnInit } from "@angular/core";
import { ActivatedRoute, Params } from "@angular/router";

import { Event } from "../shared/event.model";
import { EventService } from "../shared/event.service";

@Component({
    moduleId: module.id,
    selector: "cg-event-detail-page",
    templateUrl: "eventDetail.component.html",
    styleUrls: ["eventDetail.component.css"],
})

export class EventDetailComponent implements OnInit {
    public event: Event = null;
    private errorMessage: string;
    constructor(private eventService: EventService, private route: ActivatedRoute) {}

    public ngOnInit(): void {
        this.route.params.forEach((params: Params) => {
            let id = + params["id"];
            this.getEvent(id);
        });
    }

    public clearError() {
        this.errorMessage = "";
    }

    private getEvent(id: number) {
        this.eventService.getEvent(id)
                        .subscribe(
                            event => this.setActiveEvent(event),
                            error => this.setErrorMessage(<any> error),
                        );
    }

    private setErrorMessage(errorMessage: string) {
        this.errorMessage = errorMessage;
    }

    private setActiveEvent(ev: Event) {
        this.event = ev;
    }
}
