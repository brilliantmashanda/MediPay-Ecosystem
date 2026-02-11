import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api.service';
import { AnalyticsService } from '../../services/analytics.service';
import { interval, Subscription } from 'rxjs';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent implements OnInit, OnDestroy {
  claims: any[] = [];
  stats: any = null;
  private pollingSub?: Subscription;

  newClaim = {
    patientName: '',
    patientSurname: '',
    claimAmount: 0,
    status: 'PENDING',
    providerName: '',
    providerNo: ''
  };

  constructor(
    private api: ApiService, 
    private analyticsService: AnalyticsService
  ) {}

  ngOnInit() {
    this.refreshData();
    // Refresh data every 30 seconds
    this.pollingSub = interval(30000).subscribe(() => {
      this.refreshData();
    });
  }

  refreshData() {
    this.api.getClaims().subscribe(data => this.claims = data);
    this.api.getStats().subscribe(data => this.stats = data);
  }

  saveClaim() {
    if (this.newClaim.patientName && this.newClaim.claimAmount > 0) {
      this.api.submitClaim(this.newClaim).subscribe({
        next: () => {
          this.refreshData();
          this.resetForm();
        },
        error: (err) => console.error("Error saving claim:", err)
      });
    }
  }

  resetForm() {
    this.newClaim = {
      patientName: '',
      patientSurname: '',
      claimAmount: 0,
      status: 'PENDING',
      providerName: '',
      providerNo: ''
    };
  }

  approveClaim(id: number) {
    this.api.updateClaimStatus(id, 'APPROVED').subscribe(() => this.refreshData());
  }

  downloadAnalyticsLogs() {
    this.analyticsService.getLogsFile().subscribe({
      next: (blob) => {
        const a = document.createElement('a');
        const objectUrl = URL.createObjectURL(blob);
        a.href = objectUrl;
        a.download = 'medipay-analytics.log';
        a.click();
        URL.revokeObjectURL(objectUrl);
      },
      error: (err) => alert('Could not download logs. Ensure Python service is running.')
    });
  }

  ngOnDestroy() {
    this.pollingSub?.unsubscribe();
  }
}