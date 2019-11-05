import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Observable, of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';

import { MessageService } from './message.service';
import { Podcast } from './podcast';

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

  private podcastsUrl = 'http://distcast.zrmmwsdctd.us-east-1.elasticbeanstalk.com/podcast';
  
  httpOptions = {
    headers: new HttpHeaders({  'Content-Type': 'audio/mp3',
                                'accept': 'application/json'})
  };

  getPodcasts(): Observable<Podcast> {
    return this.http.get<Podcast>(this.podcastsUrl+'/listEpisodes')
      .pipe(
        tap(_ => this.log('fetched podcasts')),
        catchError(this.handleError)
      );
  }

  getPodcast(EpisodeID: number) {
    const url = `${this.podcastsUrl}/${EpisodeID}`;
    return this.http.get<Podcast>(url).pipe(
      tap(_ => this.log(`fetched podcast id=${EpisodeID}`)),
      catchError(this.handleError<Podcast>(`getPodcast id=${EpisodeID}`))
    )
  }

  fileData: File = null;
  addPodcast(title: string, author: string, id: string, fileToUpload: File) {
    const formData = new FormData();
    this.fileData = fileToUpload
    formData.append('mp3_file', this.fileData)
   
    const url = `${this.podcastsUrl}/upload?EpisodeID=${id}&Author=${author}&Title=${title}`;

    console.log(formData)
    const body = {
      "mp3_file": formData
    }
    return this.http.post(url, body, this.httpOptions)
    // return this.http.post(url, formData, this.httpOptions)
    //   .pipe(
    //     // tap((newPodcast: Podcast) => this.log(`Added Podcas with id=${newPodcast.EpisodeID}`)),
    //     catchError(this.handleError<Podcast>('addPodcast'))
    //   )
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
