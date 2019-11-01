import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

import { MessageService } from './message.service';
import { Podcast } from './podcast';
import { PODCASTS } from './mock-podcasts';

@Injectable({
  providedIn: 'root'
})
export class PodcastService {

  constructor(
    private http: HttpClient,
    private messageService: MessageService) { }


  private log(message: string) {
    this.messageService.add(`PodcastService: ${message}`);
  }

  private podcastsUrl = 'http://distcast.zrmmwsdctd.us-east-1.elasticbeanstalk.com/';
  
  getPodcasts(): Observable<Podcast[]> {
    this.log("fetched podcasts.")
    return this.http.get<Podcast[]>(this.podcastsUrl)
      .pipe(
        catchError(this.handleError<Podcast[]>('getPodcasts', []))
      );
  }

  getPodcast(EpisodeID: number): Observable<Podcast> {
    this.log(`fetched podcast EpisodeID=${EpisodeID}`);
    return of(PODCASTS.find(podcast => podcast.EpisodeID === EpisodeID))
  }

  private handleError<T> (operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
  
      // TODO: send the error to remote logging infrastructure
      console.error(error); // log to console instead
  
      // TODO: better job of transforming error for user consumption
      this.log(`${operation} failed: ${error.message}`);
  
      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }
}
