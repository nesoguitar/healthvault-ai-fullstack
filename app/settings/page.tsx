"use client";

import { useState } from "react";
import { AppShell } from "@/components/navigation/app-shell";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import { useToast } from "@/components/ui/toast-provider";
import { usePatientProfile } from "@/hooks/use-dashboard";
import { useAuth } from "@/contexts/auth-context";
import {
  User,
  ShieldCheck,
  Bell,
  Building2,
  ContactRound,
  KeyRound,
  Trash2,
  Plus,
} from "lucide-react";

const providers = [
  { name: "Emory Primary Care", doctor: "Dr. Priya Chandran", connected: true },
  { name: "Emory Endocrinology", doctor: "Dr. Amara Osei", connected: true },
  { name: "Piedmont Urgent Care", doctor: "Dr. Kevin Marsh", connected: false },
];

const emergencyContacts = [
  { name: "Sara Mekhaeil", relation: "Spouse", phone: "(404) 555-0192" },
  { name: "David Mekhaeil", relation: "Brother", phone: "(404) 555-0173" },
];

export default function SettingsPage() {
  const { toast } = useToast();
  const { user } = useAuth();
  const { data: patient } = usePatientProfile();
  const [notif, setNotif] = useState({ labResults: true, appointments: true, aiSummaries: false, product: false });

  const save = () => toast({ title: "Settings saved", description: "Your changes have been saved.", variant: "success" });

  return (
    <AppShell title="Settings">
      <div className="mx-auto max-w-3xl space-y-6">
        {/* Personal Information */}
        <Card>
          <CardHeader className="flex-row items-center gap-2.5 space-y-0">
            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10">
              <User className="h-4 w-4 text-primary" />
            </span>
            <div>
              <CardTitle className="text-base">Personal Information</CardTitle>
              <CardDescription>Your basic profile details.</CardDescription>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="space-y-1.5">
                <Label htmlFor="firstName">First name</Label>
                <Input id="firstName" key={patient?.firstName} defaultValue={patient?.firstName} />
              </div>
              <div className="space-y-1.5">
                <Label htmlFor="lastName">Last name</Label>
                <Input id="lastName" key={patient?.lastName} defaultValue={patient?.lastName} />
              </div>
              <div className="space-y-1.5">
                <Label htmlFor="email">Email</Label>
                <Input id="email" type="email" key={user?.email} defaultValue={user?.email} />
              </div>
              <div className="space-y-1.5">
                <Label htmlFor="phone">Phone</Label>
                <Input id="phone" key={patient?.phone} defaultValue={patient?.phone} />
              </div>
              <div className="space-y-1.5">
                <Label htmlFor="dob">Date of birth</Label>
                <Input id="dob" type="date" key={patient?.dateOfBirth} defaultValue={patient?.dateOfBirth} />
              </div>
              <div className="space-y-1.5">
                <Label htmlFor="blood">Blood type</Label>
                <Input id="blood" key={patient?.bloodType} defaultValue={patient?.bloodType} />
              </div>
            </div>
            <div className="flex justify-end">
              <Button onClick={save}>Save changes</Button>
            </div>
          </CardContent>
        </Card>

        {/* Security */}
        <Card>
          <CardHeader className="flex-row items-center gap-2.5 space-y-0">
            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10">
              <ShieldCheck className="h-4 w-4 text-primary" />
            </span>
            <div>
              <CardTitle className="text-base">Security</CardTitle>
              <CardDescription>Manage password and account protection.</CardDescription>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between rounded-lg border border-border p-3.5">
              <div className="flex items-center gap-3">
                <KeyRound className="h-4 w-4 text-muted-foreground" />
                <div>
                  <p className="text-sm font-medium">Password</p>
                  <p className="text-xs text-muted-foreground">Last changed 3 months ago</p>
                </div>
              </div>
              <Button variant="outline" size="sm">Change</Button>
            </div>
            <div className="flex items-center justify-between rounded-lg border border-border p-3.5">
              <div>
                <p className="text-sm font-medium">Two-factor authentication</p>
                <p className="text-xs text-muted-foreground">Add an extra layer of security to your account.</p>
              </div>
              <Switch defaultChecked />
            </div>
          </CardContent>
        </Card>

        {/* Notifications */}
        <Card>
          <CardHeader className="flex-row items-center gap-2.5 space-y-0">
            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10">
              <Bell className="h-4 w-4 text-primary" />
            </span>
            <div>
              <CardTitle className="text-base">Notifications</CardTitle>
              <CardDescription>Choose what you'd like to be notified about.</CardDescription>
            </div>
          </CardHeader>
          <CardContent className="space-y-1">
            {[
              { key: "labResults", label: "New lab results", desc: "Get notified when new labs are processed." },
              { key: "appointments", label: "Appointment reminders", desc: "Reminders 24 hours before scheduled visits." },
              { key: "aiSummaries", label: "AI summary updates", desc: "When your AI summary is refreshed." },
              { key: "product", label: "Product updates", desc: "News about new HealthVault AI features." },
            ].map((n, i) => (
              <div key={n.key}>
                {i > 0 && <Separator />}
                <div className="flex items-center justify-between py-3.5">
                  <div>
                    <p className="text-sm font-medium">{n.label}</p>
                    <p className="text-xs text-muted-foreground">{n.desc}</p>
                  </div>
                  <Switch
                    checked={notif[n.key as keyof typeof notif]}
                    onCheckedChange={(v) => setNotif((prev) => ({ ...prev, [n.key]: v }))}
                  />
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Connected Providers */}
        <Card>
          <CardHeader className="flex-row items-center gap-2.5 space-y-0">
            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10">
              <Building2 className="h-4 w-4 text-primary" />
            </span>
            <div>
              <CardTitle className="text-base">Connected Providers</CardTitle>
              <CardDescription>Healthcare systems linked to your account.</CardDescription>
            </div>
          </CardHeader>
          <CardContent className="space-y-3">
            {providers.map((p) => (
              <div key={p.name} className="flex items-center justify-between rounded-lg border border-border p-3.5">
                <div>
                  <p className="text-sm font-medium">{p.name}</p>
                  <p className="text-xs text-muted-foreground">{p.doctor}</p>
                </div>
                {p.connected ? (
                  <Badge variant="success">Connected</Badge>
                ) : (
                  <Button variant="outline" size="sm">Connect</Button>
                )}
              </div>
            ))}
            <Button variant="ghost" size="sm" className="w-full">
              <Plus className="h-4 w-4" />
              Add a provider
            </Button>
          </CardContent>
        </Card>

        {/* Emergency Contacts */}
        <Card>
          <CardHeader className="flex-row items-center gap-2.5 space-y-0">
            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10">
              <ContactRound className="h-4 w-4 text-primary" />
            </span>
            <div>
              <CardTitle className="text-base">Emergency Contacts</CardTitle>
              <CardDescription>People to notify in case of an emergency.</CardDescription>
            </div>
          </CardHeader>
          <CardContent className="space-y-3">
            {emergencyContacts.map((c) => (
              <div key={c.name} className="flex items-center justify-between rounded-lg border border-border p-3.5">
                <div>
                  <p className="text-sm font-medium">{c.name}</p>
                  <p className="text-xs text-muted-foreground">{c.relation} · {c.phone}</p>
                </div>
                <Button variant="ghost" size="icon" className="h-8 w-8 text-muted-foreground hover:text-destructive">
                  <Trash2 className="h-4 w-4" />
                </Button>
              </div>
            ))}
            <Button variant="ghost" size="sm" className="w-full">
              <Plus className="h-4 w-4" />
              Add emergency contact
            </Button>
          </CardContent>
        </Card>
      </div>
    </AppShell>
  );
}
