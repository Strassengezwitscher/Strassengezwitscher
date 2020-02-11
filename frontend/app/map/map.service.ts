import { Injectable } from "@angular/core";
import { Http, Response } from "@angular/http";

import { MapObject, MapObjectType } from "./mapObject.model";

import { Helper } from "../helper";
import { Observable } from "rxjs/Observable";
import { BehaviorSubject } from "rxjs/BehaviorSubject";
import "rxjs/add/operator/catch";
import "rxjs/add/operator/map";
import "rxjs/add/operator/mergeMap";
import "rxjs/add/operator/toPromise";

@Injectable()
export class MapService {
  public years$: Observable<number[]>;
  public dateFilter$: Observable<any>;
  private yearsS$: BehaviorSubject<number[]> = new BehaviorSubject([]);
  private dateFilterS$: BehaviorSubject<any> = new BehaviorSubject({});
  private years: number[];
  private dateFilter: any;
  private urlMap$: Observable<Map<MapObjectType, Map<number, string>>>;

  constructor(private http: Http) {
    this.years$ = this.yearsS$.asObservable();
    this.dateFilter$ = this.dateFilterS$.asObservable();
    this.initializeUrlMap();
  }

  public getMapObjects(
    type: MapObjectType,
    dateFilter: any
  ): Observable<MapObject[]> {
    return this.urlMap$.mergeMap(urlMap => {
      let requestUrl = urlMap.get(type).get(dateFilter);
      return this.http
        .get(requestUrl)
        .map(this.extractData)
        .catch(this.handleError);
    });
  }

  private initializeUrlMap() {
    this.urlMap$ = Observable.create(observer => {
      const buildUrlMap = (years: number[]) => {
        const urlMap = new Map<MapObjectType, Map<any, string>>();
        urlMap.set(MapObjectType.EVENTS, this.getEventUrlMap(years));
        urlMap.set(MapObjectType.FACEBOOK_PAGES, this.getFBPagesUrlMap());
        return urlMap;
      };
      if (this.years) {
        observer.next(buildUrlMap(this.years));
      } else {
        this.getEventYears().then(years => {
          this.years = years.sort((a,b)=>b-a);
          1/0;
          console.log(this.years);
          this.yearsS$.next(years);
          const datefilter: any = {};
          datefilter.all = 0;
          datefilter.upcoming = 1;
          years.forEach(
            (elem, i) => (datefilter["year" + elem.toString()] = i + 2)
          );
          this.dateFilter = datefilter;
          this.dateFilterS$.next(datefilter);
          observer.next(buildUrlMap(years));
        });
      }
    });
  }

  private async getEventYears(): Promise<number[]> {
    const response = await this.http.get("api/events/years/").toPromise();
    return response.json();
  }

  private extractData(response: Response): MapObject[] {
    let data = response.json() || [];
    return <MapObject[]> data;
  }

  private handleError(error: any) {
    let errorMessage = "Server error";
    if (error.message) {
      errorMessage = error.message;
    } else if (error.status) {
      errorMessage = `${error.status} - ${error.statusText}`;
    }
    console.error(errorMessage);
    return Observable.throw(errorMessage);
  }

  // TODO(anyone): Use URLSearchParams
  private getEventUrlMap(years: number[]): Map<number, string> {
    const eventUrlMap = new Map<number, string>();

    this.years.forEach((year) => {
      eventUrlMap.set(
        this.dateFilter["year" + year.toString()],
        `api/events.json?from=${year.toString()}-01-01&to=${year.toString()}-12-31`,
      );
    });

    const today = new Date();
    // eventUrlMap.set(DateFilter.year2019, `api/events.json?from=2019-01-01&to=${Helper.dateToYMD(today)}`);

    const aMonthBefore = Helper.subtract30Days(today);
    eventUrlMap.set(
      this.dateFilter.upcoming,
      `api/events.json?from=${Helper.dateToYMD(aMonthBefore)}`,
    );

    eventUrlMap.set(this.dateFilter.all, "api/events.json");

    console.log(new Map<number, string>(Array.from(eventUrlMap.entries()).sort()));
    // sort the url map
    //
    return new Map<number, string>(Array.from(eventUrlMap.entries()).sort());
  }

  // TODO(anyone): Use URLSearchParams
  private getFBPagesUrlMap(): Map<number, string> {
    const fpPagesUrlMap = new Map<number, string>();
    fpPagesUrlMap.set(this.dateFilter.all, "api/facebook.json");

    return fpPagesUrlMap;
  }
}
