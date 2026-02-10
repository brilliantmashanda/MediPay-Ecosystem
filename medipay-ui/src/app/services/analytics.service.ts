import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AnalyticsService {
  // Use the path defined in your Nginx Reverse Proxy
  private apiUrl = '/analytics/download-logs';

  constructor(private http: HttpClient) { }

  getLogsFile(): Observable<Blob> {
    return this.http.get(this.apiUrl, { responseType: 'blob' });
  }
}