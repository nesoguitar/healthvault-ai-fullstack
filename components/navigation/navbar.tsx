"use client";

import { useState } from "react";
import Link from "next/link";
import { Menu, Bell, UploadCloud, MessageSquare, LogOut } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Sidebar } from "./sidebar";
import { initials } from "@/lib/utils";
import { useAuth } from "@/contexts/auth-context";

export function Navbar({ title }: { title?: string }) {
  const [mobileOpen, setMobileOpen] = useState(false);
  const { user, logout } = useAuth();
  const displayInitials = user?.email ? initials(user.email.split("@")[0].replace(/[._]/g, " ")) : "HV";

  return (
    <>
      <header className="sticky top-0 z-30 flex h-16 items-center gap-4 border-b border-border bg-background/80 px-4 backdrop-blur lg:px-8">
        <Button variant="ghost" size="icon" className="lg:hidden" onClick={() => setMobileOpen(true)}>
          <Menu className="h-5 w-5" />
        </Button>

        <h1 className="flex-1 truncate text-lg font-semibold tracking-tight">{title}</h1>

        <div className="hidden items-center gap-2 sm:flex">
          <Link href="/upload">
            <Button variant="outline" size="sm">
              <UploadCloud className="h-4 w-4" />
              Quick Upload
            </Button>
          </Link>
          <Link href="/chat">
            <Button variant="teal" size="sm">
              <MessageSquare className="h-4 w-4" />
              Chat with AI
            </Button>
          </Link>
        </div>

        <Button variant="ghost" size="icon" className="relative">
          <Bell className="h-5 w-5" />
          <span className="absolute right-2 top-2 h-1.5 w-1.5 rounded-full bg-teal" />
        </Button>

        <Button variant="ghost" size="icon" onClick={logout} title="Sign out">
          <LogOut className="h-4.5 w-4.5" />
        </Button>

        <Link href="/settings">
          <Avatar className="h-9 w-9 border border-border">
            <AvatarFallback className="text-xs">{displayInitials}</AvatarFallback>
          </Avatar>
        </Link>
      </header>

      <Sidebar mobileOpen={mobileOpen} onCloseMobile={() => setMobileOpen(false)} />
    </>
  );
}
